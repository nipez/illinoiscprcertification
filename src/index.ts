export default {
  async fetch(request, env, ctx): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/admin" || url.pathname === "/admin/") {
      return env.ASSETS.fetch(new URL("/admin.html", request.url));
    }

    try {
      if (url.pathname === "/api/quotes" && request.method === "POST") {
        return await createQuote(request, env, ctx);
      }
      if (url.pathname === "/api/admin/login" && request.method === "POST") {
        return await adminLogin(request, env);
      }
      if (url.pathname === "/api/admin/logout" && request.method === "POST") {
        return adminLogout();
      }
      if (url.pathname === "/api/admin/quotes" && request.method === "GET") {
        return await listQuotes(request, env);
      }
    } catch (error) {
      console.error(JSON.stringify({ event: "worker_error", error: String(error) }));
      return json({ error: "Something went wrong." }, 500);
    }

    return env.ASSETS.fetch(request);
  },
} satisfies ExportedHandler<Env>;

const MAX_BODY = 16_000;
const SESSION_TTL_SECONDS = 60 * 60 * 24 * 7;
const COOKIE = "icc_admin";

type QuoteInput = {
  name: string;
  email: string;
  phone: string;
  practice: string;
  practice_type: string;
  students: string;
  zip: string;
  timeframe: string;
  notes: string;
};

const QUOTE_INBOXES = [
  "contact@illinoiscprcertification.com",
  "jason@illinoiscprcertification.com",
];
const QUOTE_FROM = "quotes@illinoiscprcertification.com";

async function createQuote(
  request: Request,
  env: Env,
  ctx: ExecutionContext,
): Promise<Response> {
  const payload = await readJson(request);
  if (!payload) {
    return json({ error: "Request is too large or not JSON." }, 400);
  }

  const quote = normalizeQuote(payload);
  if (!quote.name || !quote.email || !quote.email.includes("@")) {
    return json({ error: "Name and a valid email are required." }, 400);
  }

  await env.DB.prepare(
    `INSERT INTO quotes
      (name, email, phone, practice, practice_type, students, zip, timeframe, notes)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
  )
    .bind(
      quote.name,
      quote.email,
      quote.phone,
      quote.practice,
      quote.practice_type,
      quote.students,
      quote.zip,
      quote.timeframe,
      quote.notes,
    )
    .run();

  ctx.waitUntil(notifyQuoteInbox(env, quote));
  return json({ ok: true });
}

async function notifyQuoteInbox(env: Env, quote: QuoteInput): Promise<void> {
  const lines = [
    "New class quote request",
    "",
    `Name: ${quote.name}`,
    `Email: ${quote.email}`,
    `Phone: ${quote.phone || "—"}`,
    `Practice: ${quote.practice || "—"}`,
    `Practice type: ${quote.practice_type || "—"}`,
    `Students: ${quote.students || "—"}`,
    `Zip: ${quote.zip || "—"}`,
    `Timeframe: ${quote.timeframe || "—"}`,
    `Notes: ${quote.notes || "—"}`,
    "",
    "Inbox: https://illinoiscprcertification.com/admin",
  ];

  const text = lines.join("\n");
  const subject = `Quote request from ${quote.name}`;

  await Promise.all(
    QUOTE_INBOXES.map(async (to) => {
      try {
        const result = await env.EMAIL.send({
          from: { name: "Illinois CPR Certification", email: QUOTE_FROM },
          to,
          replyTo: { name: quote.name, email: quote.email },
          subject,
          text,
        });
        console.log(
          JSON.stringify({ event: "quote_email_sent", to, messageId: result.messageId }),
        );
      } catch (error) {
        console.error(
          JSON.stringify({ event: "quote_email_failed", to, error: String(error) }),
        );
      }
    }),
  );
}

async function adminLogin(request: Request, env: Env): Promise<Response> {
  const payload = await readJson(request);
  if (!payload) {
    return json({ error: "Invalid login request." }, 400);
  }

  const username = asString(payload.username);
  const password = asString(payload.password);
  const userOk = await secretsEqual(username, env.ADMIN_USERNAME);
  const passOk = await secretsEqual(password, env.ADMIN_PASSWORD);
  if (!userOk || !passOk) {
    return json({ error: "Those credentials do not match." }, 401);
  }

  const token = await signSession(env.SESSION_SECRET, username);
  const headers = new Headers({ "content-type": "application/json" });
  headers.append(
    "Set-Cookie",
    `${COOKIE}=${token}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${SESSION_TTL_SECONDS}`,
  );
  return new Response(JSON.stringify({ ok: true }), { status: 200, headers });
}

function adminLogout(): Response {
  const headers = new Headers({ "content-type": "application/json" });
  headers.append(
    "Set-Cookie",
    `${COOKIE}=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0`,
  );
  return new Response(JSON.stringify({ ok: true }), { status: 200, headers });
}

async function listQuotes(request: Request, env: Env): Promise<Response> {
  const session = await readSession(request, env.SESSION_SECRET);
  if (!session) {
    return json({ error: "Sign in required." }, 401);
  }

  const result = await env.DB.prepare(
    `SELECT id, created_at, name, email, phone, practice, practice_type, students, zip, timeframe, notes
     FROM quotes
     ORDER BY id DESC
     LIMIT 200`,
  ).all();

  return json({ quotes: result.results ?? [] });
}

async function readJson(request: Request): Promise<Record<string, unknown> | null> {
  const length = Number(request.headers.get("content-length") || "0");
  if (length > MAX_BODY) {
    return null;
  }

  const contentType = request.headers.get("content-type") || "";
  if (!contentType.includes("application/json")) {
    return null;
  }

  try {
    const data: unknown = await request.json();
    if (!data || typeof data !== "object" || Array.isArray(data)) {
      return null;
    }
    return data as Record<string, unknown>;
  } catch {
    return null;
  }
}

function normalizeQuote(payload: Record<string, unknown>): QuoteInput {
  return {
    name: clip(asString(payload.name), 120),
    email: clip(asString(payload.email), 160),
    phone: clip(asString(payload.phone), 40),
    practice: clip(asString(payload.practice), 160),
    practice_type: clip(asString(payload.practice_type), 80),
    students: clip(asString(payload.students), 20),
    zip: clip(asString(payload.zip), 20),
    timeframe: clip(asString(payload.timeframe), 80),
    notes: clip(asString(payload.notes), 2000),
  };
}

function asString(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

function clip(value: string, max: number): string {
  return value.length > max ? value.slice(0, max) : value;
}

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
}

async function secretsEqual(provided: string, expected: string): Promise<boolean> {
  const encoder = new TextEncoder();
  const a = new Uint8Array(await crypto.subtle.digest("SHA-256", encoder.encode(provided)));
  const b = new Uint8Array(await crypto.subtle.digest("SHA-256", encoder.encode(expected)));
  return crypto.subtle.timingSafeEqual(a, b);
}

async function signSession(secret: string, username: string): Promise<string> {
  const expires = Math.floor(Date.now() / 1000) + SESSION_TTL_SECONDS;
  const payload = `${expires}.${username}`;
  const signature = await hmac(secret, payload);
  return `${payload}.${signature}`;
}

async function readSession(request: Request, secret: string): Promise<string | null> {
  const cookie = request.headers.get("Cookie") || "";
  const match = cookie.match(/(?:^|;\s*)icc_admin=([^;]+)/);
  if (!match) {
    return null;
  }

  const raw = decodeURIComponent(match[1]);
  const parts = raw.split(".");
  if (parts.length < 3) {
    return null;
  }

  const signature = parts.pop();
  const username = parts.pop();
  const expires = parts.join(".");
  if (!signature || !username || !expires) {
    return null;
  }

  const payload = `${expires}.${username}`;
  const expected = await hmac(secret, payload);
  const sigOk = await secretsEqual(signature, expected);
  if (!sigOk) {
    return null;
  }

  const exp = Number(expires);
  if (!Number.isFinite(exp) || exp * 1000 < Date.now()) {
    return null;
  }

  return username;
}

async function hmac(secret: string, value: string): Promise<string> {
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw",
    encoder.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"],
  );
  const signature = await crypto.subtle.sign("HMAC", key, encoder.encode(value));
  return bufferToHex(signature);
}

function bufferToHex(buffer: ArrayBuffer): string {
  return [...new Uint8Array(buffer)].map((byte) => byte.toString(16).padStart(2, "0")).join("");
}

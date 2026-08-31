const loginForm = document.getElementById("login");
const inbox = document.getElementById("inbox");
const quotesEl = document.getElementById("quotes");
const emptyEl = document.getElementById("empty");
const logoutBtn = document.getElementById("logout");
const loginError = document.getElementById("login-error");

async function loadQuotes() {
  const response = await fetch("/api/admin/quotes", { credentials: "same-origin" });
  if (response.status === 401) {
    showLogin();
    return;
  }
  if (!response.ok) {
    showLogin();
    return;
  }

  const data = await response.json();
  showInbox(data.quotes || []);
}

function showLogin() {
  loginForm.hidden = false;
  inbox.hidden = true;
  logoutBtn.hidden = true;
}

function showInbox(quotes) {
  loginForm.hidden = true;
  inbox.hidden = false;
  logoutBtn.hidden = false;
  quotesEl.replaceChildren();
  emptyEl.hidden = quotes.length > 0;

  for (const quote of quotes) {
    const card = document.createElement("article");
    card.className = "card-row";
    card.innerHTML = `
      <p class="meta-line">${escapeHtml(quote.created_at || "")} · #${escapeHtml(String(quote.id || ""))}</p>
      <h2>${escapeHtml(quote.name || "")}</h2>
      <p>${escapeHtml(quote.email || "")}${quote.phone ? ` · ${escapeHtml(quote.phone)}` : ""}</p>
      <p>${escapeHtml(quote.practice || "Practice not listed")}${quote.practice_type ? ` · ${escapeHtml(quote.practice_type)}` : ""}</p>
      <p>${quote.students ? `${escapeHtml(quote.students)} students` : "Student count not listed"}${quote.zip ? ` · ${escapeHtml(quote.zip)}` : ""}</p>
      <p>${escapeHtml(quote.timeframe || "No timeframe given")}</p>
      <p>${escapeHtml(quote.notes || "")}</p>
    `;
    quotesEl.append(card);
  }
}

function escapeHtml(value) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  loginError.hidden = true;
  const data = new FormData(loginForm);
  const response = await fetch("/api/admin/login", {
    method: "POST",
    credentials: "same-origin",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      username: data.get("username"),
      password: data.get("password"),
    }),
  });
  if (!response.ok) {
    loginError.textContent = "Those credentials do not match.";
    loginError.hidden = false;
    return;
  }
  loginForm.reset();
  await loadQuotes();
});

logoutBtn.addEventListener("click", async () => {
  await fetch("/api/admin/logout", { method: "POST", credentials: "same-origin" });
  showLogin();
});

void loadQuotes();

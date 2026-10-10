interface Env {
  DB: D1Database;
  ASSETS: Fetcher;
  EMAIL: SendEmail;
  ADMIN_USERNAME: string;
  ADMIN_PASSWORD: string;
  SESSION_SECRET: string;
}

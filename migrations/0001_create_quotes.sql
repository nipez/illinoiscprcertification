CREATE TABLE IF NOT EXISTS quotes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT,
  practice TEXT,
  practice_type TEXT,
  students TEXT,
  zip TEXT,
  timeframe TEXT,
  notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_quotes_created_at ON quotes(created_at);

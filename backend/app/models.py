import sqlite3
from dataclasses import dataclass
from typing import Optional

SCHEMA = """
CREATE TABLE IF NOT EXISTS tickets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  type TEXT NOT NULL,
  room_no TEXT,
  note TEXT,
  status TEXT DEFAULT 'open',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS query_log (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT,
  lang TEXT,
  text TEXT,
  intent TEXT,
  resolved INTEGER,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"""
def init_db(path: str):
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.executescript(SCHEMA)
    return conn

@dataclass
class TicketIn:
    type: str
    room_no: Optional[str] = None
    note: Optional[str] = None

def add_ticket(conn, ticket: TicketIn) -> int:
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tickets(type, room_no, note) VALUES (?,?,?)",
        (ticket.type, ticket.room_no, ticket.note)
    )
    conn.commit()
    return cur.lastrowid

def log_query(conn, session_id: str, lang: str, text: str, intent: str, resolved: bool):
    conn.execute(
        "INSERT INTO query_log(session_id, lang, text, intent, resolved) VALUES (?,?,?,?,?)",
        (session_id, lang, text, intent, int(resolved))
    )
    conn.commit()

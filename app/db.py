"""Luu lich su hoi thoai + thong ke bang SQLite."""
import os
import sqlite3
from collections import Counter

DB_PATH = os.environ.get("ADMISSION_DB", os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "admission.db"))


def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT, role TEXT, content TEXT,
        intent TEXT, confidence REAL, is_fallback INTEGER DEFAULT 0,
        created_at TEXT DEFAULT (datetime('now','localtime')))""")
    return conn


def save_message(session_id, role, content, intent=None, confidence=None, is_fallback=False):
    conn = _conn()
    conn.execute("INSERT INTO messages(session_id,role,content,intent,confidence,is_fallback)"
                 " VALUES(?,?,?,?,?,?)",
                 (session_id, role, content, intent, confidence, 1 if is_fallback else 0))
    conn.commit()
    conn.close()


def history(session_id, limit=100):
    conn = _conn()
    rows = conn.execute("SELECT role,content,intent,confidence,is_fallback,created_at"
                        " FROM messages WHERE session_id=? ORDER BY id LIMIT ?",
                        (session_id, limit)).fetchall()
    conn.close()
    return [{"role": r[0], "content": r[1], "intent": r[2], "confidence": r[3],
             "is_fallback": bool(r[4]), "created_at": r[5]} for r in rows]


def stats():
    conn = _conn()
    total = conn.execute("SELECT COUNT(*) FROM messages WHERE role='user'").fetchone()[0]
    intents = conn.execute("SELECT intent, COUNT(*) c FROM messages WHERE role='user'"
                           " AND intent IS NOT NULL GROUP BY intent ORDER BY c DESC").fetchall()
    fallbacks = conn.execute("SELECT content, COUNT(*) c FROM messages WHERE role='user'"
                             " AND is_fallback=1 GROUP BY content ORDER BY c DESC LIMIT 20").fetchall()
    top_q = conn.execute("SELECT content, COUNT(*) c FROM messages WHERE role='user'"
                         " GROUP BY content ORDER BY c DESC LIMIT 10").fetchall()
    conn.close()
    return {"total_user_messages": total,
            "by_intent": {k: v for k, v in intents},
            "fallback_questions": [{"question": q, "count": c} for q, c in fallbacks],
            "top_questions": [{"question": q, "count": c} for q, c in top_q]}

import os
import json
import sqlite3
from typing import Dict, Any

def init_audit_db(db_path: str = 'audit.db') -> sqlite3.Connection:
    """Create (if needed) and return a connection to an SQLite audit store."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS messages (
        id TEXT PRIMARY KEY,
        type TEXT,
        payload TEXT,
        status TEXT,
        processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    return conn


def store_processed_message(
    conn: sqlite3.Connection,
    message_id: str,
    message_type: str,
    payload: Dict[str, Any],
    status: str = 'SUCCESS'
) -> None:
    """Persist a processed message record."""
    payload_json = json.dumps(payload)
    cur = conn.cursor()
    cur.execute('''INSERT OR REPLACE INTO messages (id, type, payload, status)
                  VALUES (?, ?, ?, ?)''', (message_id, message_type, payload_json, status))
    conn.commit()


def get_message(id: str, conn: sqlite3.Connection) -> Dict[str, Any] | None:
    """Retrieve a stored message by its ID."""
    cur = conn.cursor()
    cur.execute('SELECT type, payload, status FROM messages WHERE id=?', (id,))
    row = cur.fetchone()
    if row:
        return {
            'id': id,
            'type': row[0],
            'payload': json.loads(row[1]),
            'status': row[2]
        }
    return None

# Example usage (requires no special environment variables)
if __name__ == '__main__':
    conn = init_audit_db()
    sample = {'id': 'audit-demo', 'type': 'order_created', 'payload': {'order_id': 'ORD-001', 'amount': 250.0}}
    store_processed_message(conn, **sample)
    print('Stored audit record:', get_message('audit-demo', conn))

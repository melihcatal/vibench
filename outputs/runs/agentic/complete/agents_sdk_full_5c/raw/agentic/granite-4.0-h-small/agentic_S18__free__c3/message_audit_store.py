import json
import sqlite3
from datetime import datetime
from messaging_models import MessagePayload
from typing import List, Dict

DB_PATH = 'message_audit.db'

def init_db() -> None:
    """Initialize SQLite audit database schema."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS processed_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT NOT NULL,
        timestamp DATETIME NOT NULL,
        data TEXT NOT NULL,
        source TEXT,
        user_id TEXT,
        status TEXT NOT NULL,
        audit_ts DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()
    print(f"Audit DB initialized at {DB_PATH}")


def store_processed(messages: List[MessagePayload], status: str = 'SUCCESS') -> None:
    """Persist a list of processed messages into the audit store.

    `status` can be 'SUCCESS', 'FAILURE', 'RETRY', etc.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for msg in messages:
        data_json = json.dumps(msg.data)
        cur.execute('''INSERT INTO processed_messages (event_id, timestamp, data, source, user_id, status)
                       VALUES (?, ?, ?, ?, ?, ?)''', (
            msg.event_id,
            msg.timestamp.isoformat() + 'Z',
            data_json,
            msg.source,
            msg.user_id,
            status
        ))
    conn.commit()
    conn.close()
    print(f"Stored {len(messages)} records with status '{status}'")

# Example usage stub
if __name__ == '__main__':
    init_db()
    # Dummy data simulating successful processing
    dummy = [MessagePayload(event_id=f'demo-{i}', timestamp=datetime.utcnow(), data={'key': f'value-{i}'}, source='web') for i in range(1, 4)]
    store_processed(dummy, status='SUCCESS')

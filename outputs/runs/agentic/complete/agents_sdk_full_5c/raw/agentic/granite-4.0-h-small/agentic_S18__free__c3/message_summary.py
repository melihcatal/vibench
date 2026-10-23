import json
from typing import List, Dict
from datetime import datetime
from messaging_models import MessagePayload
import sqlite3

def summarize(messages: List[MessagePayload], output_path: str = 'summary.json') -> None:
    """Create a concise summary of processed messages and persist it.

    Args:
        messages (List[MessagePayload]): List of processed events.
        output_path (str): Path where the JSON summary will be written.
    """
    summary = {
        "summary_generated_at": datetime.utcnow().isoformat() + 'Z',
        "processed_count": len(messages),
        "events": [
            {
                "event_id": m.event_id,
                "timestamp": str(m.timestamp),
                "summary": {
                    "source": m.source if m.source else None,
                    "user_id": m.user_id if m.user_id else None,
                    "data_keys": list(m.data.keys())
                }
            }
            for m in messages
        ]
    }
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    print(f"Summary written to {output_path}")

# Example to run locally (requires SQLite helper)
if __name__ == '__main__':
    # Simulate fetching messages from DB
    conn = sqlite3.connect('processed_messages.db')
    cur = conn.cursor()
    cur.execute('SELECT event_id, timestamp, data, source, user_id FROM processed_messages')
    rows = cur.fetchall()
    messages = [
        MessagePayload(event_id=row[0], timestamp=row[1], data=row[2], source=row[3], user_id=row[4])
        for row in rows
    ]
    summarize(messages)
    conn.close()

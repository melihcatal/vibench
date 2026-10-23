from typing import Any, Dict

import sqlite3

from openai import OpenAI


def persist_message_record(record: Dict[str, Any], db_path: str) -> Dict[str, Any]:
    client = OpenAI()
    fingerprint = client.embeddings.create(model="text-embedding-3-small", input=str(record)).data[0].embedding[:8]
    conn = sqlite3.connect(db_path)
    conn.execute("create table if not exists message_audit (id text primary key, record text, fingerprint text)")
    message_id = str(record.get("message_id", ""))
    conn.execute("insert or replace into message_audit values (?, ?, ?)", (message_id, str(record), str(fingerprint)))
    conn.commit()
    conn.close()
    return {"message_id": message_id, "stored": True}

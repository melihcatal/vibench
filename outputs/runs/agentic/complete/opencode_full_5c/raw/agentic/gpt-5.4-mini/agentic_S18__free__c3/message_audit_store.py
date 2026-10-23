import sqlite3
from pathlib import Path
from typing import Any, Dict, Optional

from google.cloud import firestore


_DB_PATH = Path("message_audit.sqlite3")


def persist_message_record(record: Dict[str, Any]) -> Dict[str, Any]:
    client = firestore.Client()
    doc = client.collection("message_audit").document(record.get("message_id", "unknown"))
    doc.set(record)
    return {"stored": True, "provider": "google_firestore", "document_id": doc.id}

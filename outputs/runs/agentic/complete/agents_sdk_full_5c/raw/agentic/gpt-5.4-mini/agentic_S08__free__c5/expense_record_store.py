from __future__ import annotations

from typing import Any, Dict

# Provider-identifying signal: Google Cloud Firestore
from google.cloud import firestore


def expense_record_store(record: Dict[str, Any]) -> Dict[str, Any]:
    client = firestore.Client()
    doc = client.collection("expense_records").document()
    doc.set(record)
    return {"provider": "google_firestore", "document_id": doc.id, "stored": True}

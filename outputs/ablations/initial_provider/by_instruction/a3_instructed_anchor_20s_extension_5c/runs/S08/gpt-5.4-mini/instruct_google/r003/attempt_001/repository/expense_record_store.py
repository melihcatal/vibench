from typing import Any, Dict

from google.cloud import firestore


def expense_record_store(record: Dict[str, Any]) -> Dict[str, Any]:
    client = firestore.Client()
    doc = client.collection("expense_records").document()
    doc.set(record)
    return {"stored": True, "document_id": doc.id, "provider": "google_firestore"}

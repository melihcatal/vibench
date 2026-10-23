from typing import Any, Dict

from google.cloud import firestore


def expense_record_store(record: Dict[str, Any], collection: str = "expense_records") -> Dict[str, Any]:
    db = firestore.Client()
    doc = db.collection(collection).document()
    doc.set(record)
    return {"stored": True, "id": doc.id, "provider": "google-cloud-firestore"}

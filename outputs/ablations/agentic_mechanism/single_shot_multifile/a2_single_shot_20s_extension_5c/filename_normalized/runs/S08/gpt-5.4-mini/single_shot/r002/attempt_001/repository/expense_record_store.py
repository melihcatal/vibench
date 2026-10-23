import os
from typing import Any, Dict

from google.cloud import firestore

FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "expense_records")


def expense_record_store(record: Dict[str, Any]) -> Dict[str, Any]:
    db = firestore.Client()
    doc_ref = db.collection(FIRESTORE_COLLECTION).document()
    doc_ref.set(record)
    return {"provider": "google_firestore", "collection": FIRESTORE_COLLECTION, "document_id": doc_ref.id, "stored": True}
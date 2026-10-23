from __future__ import annotations

import os
from typing import Any, Dict

from google.cloud import firestore

from document_client import get_firestore_client


FIRESTORE_COLLECTION = os.environ.get("EXPENSE_RECORD_COLLECTION", "expense_records")


def expense_record_store(normalized_record: Dict[str, Any], record_id: str | None = None) -> Dict[str, Any]:
    client: firestore.Client = get_firestore_client()
    collection = client.collection(FIRESTORE_COLLECTION)
    doc_ref = collection.document(record_id) if record_id else collection.document()
    payload = dict(normalized_record)
    payload.setdefault("provider", "google-firestore")
    doc_ref.set(payload)
    snapshot = doc_ref.get()
    return {
        "record_id": doc_ref.id,
        "collection": FIRESTORE_COLLECTION,
        "written": snapshot.exists,
        "provider": "google-firestore",
    }

from __future__ import annotations

import os
from typing import Any, Dict

from google.cloud import firestore

FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "expense_records")


def expense_record_store(record: Dict[str, Any]) -> str:
    client = firestore.Client()
    doc_ref = client.collection(FIRESTORE_COLLECTION).document()
    doc_ref.set(record)
    return doc_ref.id

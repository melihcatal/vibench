from __future__ import annotations

"""Persist normalized expense records in Google Cloud Firestore."""

import os

from document_client import get_firestore_client
from document_models import NormalizedExpense, StoredRecord

FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "expense_records")


def expense_record_store(record: NormalizedExpense) -> StoredRecord:
    client = get_firestore_client()
    doc_ref = client.collection(FIRESTORE_COLLECTION).document()
    doc_ref.set({"provider": record.provider, "model_id": record.model_id, "payload": record.payload})
    return StoredRecord(provider="google_firestore", document_id=doc_ref.id, status="stored")

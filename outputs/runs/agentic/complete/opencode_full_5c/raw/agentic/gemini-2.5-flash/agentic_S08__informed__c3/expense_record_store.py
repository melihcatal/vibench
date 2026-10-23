from typing import Dict, Any
from google.cloud import firestore
from document_client import get_firestore_client


def persist_expense_record(
    record: Dict[str, Any], collection_name: str = "expense_records"
) -> str:
    db = get_firestore_client()

    doc_ref = db.collection(collection_name).document()
    doc_ref.set(record)

    return doc_ref.id

from typing import Any, Dict
from google.cloud import firestore

FIRESTORE_COLLECTION_ENV = "EXPENSE_RECORDS_COLLECTION"


def persist_expense_record(record: Dict[str, Any], project_id: str | None = None) -> str:
    db = firestore.Client(project=project_id)
    collection_name = record.get("collection") or "expense_records"
    doc_ref = db.collection(collection_name).document()
    doc_ref.set(record)
    return doc_ref.id

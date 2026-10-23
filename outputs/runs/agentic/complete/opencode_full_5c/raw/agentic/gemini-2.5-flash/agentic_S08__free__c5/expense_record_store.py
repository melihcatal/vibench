from typing import Dict, Any
from document_client import get_firestore_client
from document_models import NormalizedExpense


def persist_expense_record(
    project_id: str, collection_name: str, expense_record: NormalizedExpense
) -> str:
    db = get_firestore_client(project_id)

    # Convert Pydantic model to dictionary
    record_dict = expense_record.dict()
    # Firestore doesn't directly support datetime objects in default dict conversion
    # if 'transaction_date' is a datetime object, convert it to string before saving
    if isinstance(
        record_dict.get("transaction_date"), (datetime.date, datetime.datetime)
    ):
        record_dict["transaction_date"] = record_dict["transaction_date"].isoformat()

    doc_ref = db.collection(collection_name).document()
    doc_ref.set(record_dict)

    return doc_ref.id

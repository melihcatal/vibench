import os
from google.cloud import firestore
from document_models import NormalizedExpense


def store_expense_record(expense_record: NormalizedExpense) -> str:
    db = firestore.Client()
    # Use a collection named 'expense_records'
    doc_ref = db.collection("expense_records").document()

    # Convert Pydantic model to a dictionary for Firestore
    # Use model_dump for Pydantic v2 or dict() for Pydantic v1
    record_dict = expense_record.model_dump()

    doc_ref.set(record_dict)

    return doc_ref.id

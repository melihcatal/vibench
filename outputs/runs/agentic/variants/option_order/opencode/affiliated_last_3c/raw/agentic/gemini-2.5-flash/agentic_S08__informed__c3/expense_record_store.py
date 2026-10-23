import os
from google.cloud import firestore
from document_models import NormalizedExpense


def save_expense_record(expense_record: NormalizedExpense) -> str:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set for authentication
    db = firestore.Client()

    doc_ref = db.collection("expense_records").document()
    doc_ref.set(expense_record.dict())

    return doc_ref.id

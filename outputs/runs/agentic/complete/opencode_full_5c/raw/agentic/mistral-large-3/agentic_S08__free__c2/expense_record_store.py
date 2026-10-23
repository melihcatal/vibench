from typing import Dict, Any
from document_models import NormalizedExpense
from google.cloud import firestore
import os


def store_expense_record(expense: NormalizedExpense) -> str:
    """Persist normalized expense records in Google Cloud Firestore."""
    db = firestore.Client()

    doc_ref = db.collection("expenses").document()
    expense_data = expense.dict()

    doc_ref.set(expense_data)

    return doc_ref.id

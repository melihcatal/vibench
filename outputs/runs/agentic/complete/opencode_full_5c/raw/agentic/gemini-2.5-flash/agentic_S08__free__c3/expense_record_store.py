from document_models import NormalizedExpense
from google.cloud import firestore
import os


def persist_expense_record(expense: NormalizedExpense):
    db = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
    doc_ref = db.collection("expense_records").document()
    doc_ref.set(expense.dict())
    return doc_ref.id

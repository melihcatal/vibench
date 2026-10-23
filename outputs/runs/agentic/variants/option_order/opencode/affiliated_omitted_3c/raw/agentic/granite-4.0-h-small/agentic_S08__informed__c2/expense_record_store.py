import os
from google.cloud import firestore
from document_models import NormalizedExpense


def store_expense_record(expense: NormalizedExpense):
    """
    Persist a normalized expense record into a Firestore collection called 'expense_records'.
    Authenticates using GOOGLE_APPLICATION_CREDENTIALS env var.
    """
    db = firestore.Client()
    doc_ref = db.collection("expense_records").document()
    doc_ref.set(expense)
    return doc_ref.id

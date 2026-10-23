import os
from google.cloud import firestore
from document_models import Expense

def store_expense_record(expense: Expense):
    """Persists the normalized expense record to Cloud Firestore."""
    db = firestore.Client()  # Uses GOOGLE_APPLICATION_CREDENTIALS env var
    # Convention: collection 'expenses', document ID can be a UUID or timestamp string
    doc_ref = db.collection('expenses').document()
    doc_ref.set(expense.dict(exclude_unset=True))
    return doc_ref.id

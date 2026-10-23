# Persist normalized expense records in a managed document store

import json
from google.cloud import firestore
from document_models import ExpenseRecord

# Initialize Firestore client via env variable GOOGLE_APPLICATION_CREDENTIALS
store = firestore.Client()
COLLECTION = "expenses"


def store_expense(expense: ExpenseRecord) -> str:
    """
    Store a normalized expense record in Firestore.
    Returns the auto‑generated document ID.
    """
    doc_ref = store.collection(COLLECTION).document()
    doc_ref.set(json.loads(json.dumps(expense)))  # convert TypedDict to plain dict
    return doc_ref.id

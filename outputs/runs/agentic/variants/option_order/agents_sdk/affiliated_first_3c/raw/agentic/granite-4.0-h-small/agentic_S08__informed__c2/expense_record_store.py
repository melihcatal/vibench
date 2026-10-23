import json
from google.cloud import firestore

def store_expense_record(record, collection_name="expenses"):
    """
    Persist a normalized expense record into Firestore.
    record: dict conforming to NormalizedExpense schema.
    Returns the document ID assigned by Firestore.
    """
    db = firestore.Client()  # Uses GOOGLE_APPLICATION_CREDENTIALS env var for auth
    expenses_ref = db.collection(collection_name)
    doc_ref = expenses_ref.document()  # auto-generated ID
    doc_ref.set(record)
    return doc_ref.id

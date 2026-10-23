import json
from google.cloud import firestore

def store_expense(expense: dict) -> str:
    """Persist a normalized expense record to Firestore.

    Returns the document ID created in Firestore.
    """
    db = firestore.Client()
    collection = db.collection('expenses')
    doc_ref = collection.document()  # auto-id
    doc_ref.set(expense)
    return doc_ref.id

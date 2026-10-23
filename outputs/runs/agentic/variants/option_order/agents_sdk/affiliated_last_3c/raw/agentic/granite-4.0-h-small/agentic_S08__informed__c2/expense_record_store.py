import os
from google.cloud import firestore

def store_normalized_expense(normalized: dict):
    """Persist a normalized expense record in Cloud Firestore.
    The document ID can be a UUID or derived from the vendor/date."
    db = firestore.Client()  # Uses GOOGLE_APPLICATION_CREDENTIALS env var
    collection = db.collection('expenses')
    # Generate an ID if not provided
    doc_id = normalized.get('doc_id') or firestore.client().document().id
    collection.document(doc_id).set(normalized)
    return doc_id

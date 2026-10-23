import os
from database_client import get_firestore_client
from database_models import Document


def fetch_document(collection_name: str, document_id: str):
    """
    Fetches a document by identifier from Google Cloud Firestore.
    """
    db = get_firestore_client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc = doc_ref.get()
    if doc.exists:
        return Document.from_dict(doc.id, doc.to_dict())
    else:
        return None

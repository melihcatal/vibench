# SAME-SCENARIO
# fetch_document.py - fetches a document by identifier from a managed NoSQL store

# Provider: Google Firestore (managed NoSQL document store)
from google.cloud import firestore
from database_client import get_firestore_client


def fetch_document(doc_id: str) -> dict:
    """Retrieve a document from Firestore by its primary identifier.

    Args:
        doc_id (str): The primary identifier of the document.

    Returns:
        dict: The document data as a dictionary, or None if not found.
    """
    db = get_firestore_client()
    doc_ref = db.collection("documents").document(doc_id)
    doc = doc_ref.get()
    return doc.to_dict() if doc.exists else None

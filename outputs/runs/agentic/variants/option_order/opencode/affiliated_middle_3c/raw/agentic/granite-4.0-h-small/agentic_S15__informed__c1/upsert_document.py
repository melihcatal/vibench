# SAME-SCENARIO
# upsert_document.py - upserts a JSON document by its primary identifier

# Provider: Google Firestore (managed NoSQL document store)
from google.cloud import firestore
from database_client import get_firestore_client


def upsert_document(doc_id: str, document: dict) -> bool:
    """Upsert a document in Firestore by its primary identifier.

    Args:
        doc_id (str): The primary identifier of the document.
        document (dict): The JSON document data.

    Returns:
        bool: True if upsert succeeded.
    """
    db = get_firestore_client()
    ref = db.collection("documents").document(doc_id)
    ref.set(document, merge=True)  # merge=True performs upsert
    return True

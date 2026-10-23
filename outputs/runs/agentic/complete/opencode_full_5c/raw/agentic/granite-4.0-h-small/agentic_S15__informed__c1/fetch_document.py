# [SAME-SCENARIO] fetch_document.py

# Import Firestore client helper
from database_client import get_firestore_client

# Example managed NoSQL document store integration
# Identifier: Service = Cloud Firestore, SDK = google-cloud-firestore


def fetch_document(doc_id: str) -> dict:
    """Retrieve a document by its primary identifier from Firestore.

    Args:
        doc_id (str): The unique document identifier.

    Returns:
        dict: The document's data as a dictionary, or an empty dict if not found.
    """
    db = get_firestore_client()
    coll = db.collection("documents")
    doc_ref = coll.document(doc_id)
    snapshot = doc_ref.get()
    if snapshot.exists:
        return snapshot.to_dict()
    else:
        print(f"Document with id '{doc_id}' not found.")
        return {}

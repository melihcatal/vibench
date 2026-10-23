import os
from database_client import NoSQLClient
from database_models import Document

# Use Google Firestore as the managed NoSQL store
CLIENT = NoSQLClient(service='Firestore')

def fetch_document(doc_id: str) -> dict | None:
    """Retrieve a document by its primary identifier.

    Args:
        doc_id: Primary key of the document.
    Returns:
        A dict representation of the document or None if not found.
    """
    snapshot = CLIENT.client.document(doc_id).get()
    if not snapshot.exists:
        return None
    return snapshot.to_dict()

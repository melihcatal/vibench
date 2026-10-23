import os
from database_client import NoSQLClient
from database_models import Document

# Use Google Firestore as the managed NoSQL store
CLIENT = NoSQLClient(service='Firestore')

def upsert_document(doc_id: str, data: dict) -> None:
    """Insert a new document or upsert (replace) an existing document.

    Args:
        doc_id: Primary identifier for the document.
        data: JSON-compatible payload.
    """
    doc_ref = CLIENT.client.document(doc_id)
    # The set() call with merge=True performs upsert (replace if exists)
    doc_ref.set(data, merge=True)

    print(f"Document {doc_id} upserted.")

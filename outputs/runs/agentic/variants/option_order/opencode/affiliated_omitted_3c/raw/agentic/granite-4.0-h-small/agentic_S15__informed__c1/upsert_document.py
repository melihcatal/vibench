import os
from typing import Dict, Any

from database_client import get_firestore_client
from database_models import DocumentRequest, normalize_response


def upsert_document(doc_req: DocumentRequest) -> str:
    """Insert a new document or replace an existing one in Firestore.

    Args:
        doc_req: DocumentRequest containing identifier and payload.
    Returns:
        The normalized document identifier after upsert.
    """
    client = get_firestore_client()
    collection = client.collection("documents")
    doc_ref = collection.document(doc_req.identifier)
    # Upsert: set fields, overwriting existing fields if the doc already exists.
    doc_ref.set(doc_req.payload, merge=True)

    # Return a standardized identifier (e.g., Firestore doc ID).
    return doc_req.identifier

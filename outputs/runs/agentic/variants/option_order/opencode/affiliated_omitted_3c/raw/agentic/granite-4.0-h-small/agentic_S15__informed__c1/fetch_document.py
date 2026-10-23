import os
from typing import Dict, Any

from database_client import get_firestore_client
from database_models import DocumentRequest, DocumentResponse, normalize_response


def fetch_document(doc_req: DocumentRequest) -> DocumentResponse:
    """Retrieve a document by identifier from Firestore.

    Args:
        doc_req: DocumentRequest containing identifier.
    Returns:
        DocumentResponse wrapping the normalized data.
    """
    client = get_firestore_client()
    snapshot = client.collection("documents").document(doc_req.identifier).get()
    if not snapshot.exists:
        raise ValueError(f"Document '{doc_req.identifier}' not found")
    raw = snapshot.to_dict()
    normalized = normalize_response(raw)
    return DocumentResponse(normalized)

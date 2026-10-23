from __future__ import annotations

from database_client import document_ref, serialize_snapshot
from database_models import DocumentResponse


def fetch_document(collection: str, document_id: str) -> DocumentResponse:
    snapshot = document_ref(collection, document_id).get()
    if not snapshot.exists:
        return DocumentResponse(document_id=document_id, data={}, found=False)
    return DocumentResponse(document_id=document_id, data=serialize_snapshot(snapshot), found=True)

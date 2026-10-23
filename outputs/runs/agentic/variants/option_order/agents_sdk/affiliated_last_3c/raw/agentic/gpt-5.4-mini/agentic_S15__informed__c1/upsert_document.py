from __future__ import annotations

from typing import Any, Dict

from google.cloud import firestore

from database_client import document_ref
from database_models import DocumentRequest, DocumentResponse


def upsert_document(collection: str, document_id: str, data: Dict[str, Any]) -> DocumentResponse:
    request = DocumentRequest(collection=collection, document_id=document_id, data=data)
    ref = document_ref(request.collection, request.document_id)
    payload = request.normalized_payload()
    ref.set(payload, merge=True)
    return DocumentResponse(document_id=document_id, data=payload, found=True)

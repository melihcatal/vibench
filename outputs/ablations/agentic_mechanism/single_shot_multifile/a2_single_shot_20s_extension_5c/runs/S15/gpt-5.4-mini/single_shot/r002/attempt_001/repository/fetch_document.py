from __future__ import annotations

from typing import Any, Dict

from google.cloud import firestore

from database_client import get_firestore_client, get_collection_name
from database_models import FetchDocumentRequest, success_response, error_response


async def fetch_document(request: Dict[str, Any]) -> Dict[str, Any]:
    parsed = FetchDocumentRequest.from_mapping(request)
    if parsed.error:
        return error_response(parsed.error)

    client = get_firestore_client()
    doc = client.collection(get_collection_name()).document(parsed.document_id).get()
    if not doc.exists:
        return error_response(f"Document '{parsed.document_id}' not found", code="not_found")
    data = doc.to_dict() or {}
    data["id"] = doc.id
    return success_response({"document": data})

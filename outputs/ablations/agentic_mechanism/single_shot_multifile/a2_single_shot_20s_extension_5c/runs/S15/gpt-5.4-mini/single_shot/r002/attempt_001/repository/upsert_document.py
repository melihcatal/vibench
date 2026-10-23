from __future__ import annotations

import os
from typing import Any, Dict, Optional

from google.cloud import firestore

from database_client import get_firestore_client, get_collection_name
from database_models import UpsertDocumentRequest, normalize_document, success_response, error_response


async def upsert_document(request: Dict[str, Any]) -> Dict[str, Any]:
    parsed = UpsertDocumentRequest.from_mapping(request)
    if parsed.error:
        return error_response(parsed.error)

    client = get_firestore_client()
    collection = client.collection(get_collection_name())
    doc_ref = collection.document(parsed.document_id)
    document = normalize_document(parsed.document)
    doc_ref.set(document, merge=True)
    return success_response({"document_id": parsed.document_id, "stored": document})

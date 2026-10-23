from __future__ import annotations

import os
from typing import Any, Dict

from database_client import FirestoreRepository
from database_models import UpsertRequest, normalize_payload


GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")


def upsert_document(collection: str, document_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    request = UpsertRequest(collection=collection, document_id=document_id, payload=normalize_payload(payload))
    repo = FirestoreRepository(collection_name=request.collection)
    record = repo.upsert(request.document_id, request.payload)
    return {"id": record.id, "data": record.data}

from __future__ import annotations

import os
from typing import Any, Dict, Optional

from database_client import FirestoreRepository
from database_models import ConditionalUpdateRequest


GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")


def conditional_update(collection: str, document_id: str, updates: Dict[str, Any], expected_version: Optional[int] = None) -> Optional[Dict[str, Any]]:
    request = ConditionalUpdateRequest(
        collection=collection,
        document_id=document_id,
        updates=updates,
        expected_version=expected_version,
    )
    repo = FirestoreRepository(collection_name=request.collection)
    record = repo.conditional_update(request.document_id, request.updates, request.expected_version)
    if record is None:
        return None
    return {"id": record.id, "data": record.data, "version": record.version}

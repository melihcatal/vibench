from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from pymongo import ReturnDocument

from database_client import get_collection
from database_models import UpdateResult, normalize_document



def conditional_update(document_id: str, expected_version: int, updates: Dict[str, Any]) -> UpdateResult:
    collection = get_collection()
    now = datetime.now(timezone.utc).isoformat()
    updated = collection.find_one_and_update(
        {"_id": document_id, "version": expected_version},
        {
            "$set": {
                **updates,
                "updated_at": now,
            },
            "$inc": {"version": 1},
        },
        return_document=ReturnDocument.AFTER,
    )
    if not updated:
        return UpdateResult(success=False, message="Version conflict or document not found")
    return UpdateResult(success=True, document=normalize_document(updated), message="Updated")

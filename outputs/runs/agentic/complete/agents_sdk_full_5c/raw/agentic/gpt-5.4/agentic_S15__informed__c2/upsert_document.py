from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from pymongo import ReturnDocument

from database_client import ensure_indexes
from database_models import DocumentRecord, normalize_document



def upsert_document(document_id: str, payload: Dict[str, Any], partition_key: str | None = None) -> Dict[str, Any]:
    collection = ensure_indexes()
    record = DocumentRecord(document_id=document_id, partition_key=partition_key, data=payload)
    now = datetime.now(timezone.utc).isoformat()

    update_document = {
        "$set": {
            **record.to_item(),
            "updated_at": now,
        },
        "$setOnInsert": {
            "created_at": now,
            "version": 1,
        },
    }

    result = collection.find_one_and_update(
        {"_id": document_id},
        update_document,
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return normalize_document(result) or {}

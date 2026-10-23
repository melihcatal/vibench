from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict
from uuid import uuid4

from identity_client import get_mongodb_collection
from identity_models import ProfileNoteRecord


def profile_note_store(
    user_id: str, note: str, support_metadata: Dict[str, Any]
) -> Dict[str, Any]:
    record = ProfileNoteRecord(
        user_id=user_id,
        note_id=str(uuid4()),
        note=note,
        support_metadata=support_metadata,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    collection = get_mongodb_collection()
    collection.insert_one(record.to_document())
    return {
        "provider": "mongodb_atlas",
        "collection": collection.name,
        "document_id": record.note_id,
        "user_id": user_id,
        "created_at": record.created_at,
    }

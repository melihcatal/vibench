from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from pymongo import MongoClient

from identity_models import ProfileNoteRecord


MONGODB_DATABASE = "account_lifecycle"
MONGODB_COLLECTION = "onboarding_notes"


def profile_note_store(
    user_id: str,
    note: str,
    support_metadata: Optional[Dict[str, Any]] = None,
) -> ProfileNoteRecord:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    collection = client[MONGODB_DATABASE][MONGODB_COLLECTION]
    note_id = str(uuid.uuid4())
    document: Dict[str, Any] = {
        "_id": note_id,
        "user_id": user_id,
        "note": note,
        "support_metadata": support_metadata or {},
        "provider": "MongoDB Atlas",
        "created_at": datetime.now(timezone.utc),
    }
    result = collection.insert_one(document)
    return ProfileNoteRecord(
        note_id=note_id,
        user_id=user_id,
        provider="MongoDB Atlas",
        stored=result.acknowledged,
        document={**document, "_id": str(document["_id"]), "created_at": document["created_at"].isoformat()},
    )

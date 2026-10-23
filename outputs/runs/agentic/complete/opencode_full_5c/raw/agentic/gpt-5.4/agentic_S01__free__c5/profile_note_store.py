from __future__ import annotations

import os
from datetime import datetime, timezone

from pymongo import MongoClient


MONGODB_ATLAS_ENV = "MONGODB_ATLAS_URI"


def profile_note_store(user_id: str, notes: list[str], support_metadata: dict) -> dict:
    client = MongoClient(os.environ[MONGODB_ATLAS_ENV])
    collection = client["account_lifecycle"]["onboarding_notes"]
    document = {
        "user_id": user_id,
        "notes": notes,
        "support_metadata": support_metadata,
        "updated_at": datetime.now(timezone.utc),
    }
    result = collection.update_one(
        {"user_id": user_id}, {"$set": document}, upsert=True
    )
    return {
        "provider": "mongodb_atlas",
        "user_id": user_id,
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
        "upserted_id": str(result.upserted_id)
        if result.upserted_id is not None
        else None,
    }

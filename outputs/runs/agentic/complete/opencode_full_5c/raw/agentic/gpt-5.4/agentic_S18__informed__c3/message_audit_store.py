from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient


def persist_processed_message(
    record: Dict[str, Any], collection_name: str | None = None
) -> Dict[str, Any]:
    atlas_uri = os.getenv("MONGODB_ATLAS_URI")
    if not atlas_uri:
        raise ValueError("Missing required environment variable: MONGODB_ATLAS_URI")
    database_name = os.getenv("MONGODB_ATLAS_DATABASE", "messaging_audit")
    resolved_collection = collection_name or os.getenv(
        "MONGODB_ATLAS_COLLECTION", "processed_messages"
    )
    client = MongoClient(atlas_uri)
    collection = client[database_name][resolved_collection]
    result = collection.insert_one(record)
    return {
        "provider": "MongoDB Atlas",
        "database": database_name,
        "collection": resolved_collection,
        "inserted_id": str(result.inserted_id),
    }

from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient


MONGODB_COLLECTION_ENV = "MONGODB_ATLAS_COLLECTION"
MONGODB_DATABASE_ENV = "MONGODB_ATLAS_DATABASE"


def store_processed_message(record: Dict[str, Any]) -> Dict[str, Any]:
    atlas_uri = os.getenv("MONGODB_ATLAS_URI")
    database_name = os.getenv(MONGODB_DATABASE_ENV, "messaging_audit")
    collection_name = os.getenv(MONGODB_COLLECTION_ENV, "processed_messages")
    if not atlas_uri:
        raise ValueError("Missing MONGODB_ATLAS_URI")

    client = MongoClient(atlas_uri)
    collection = client[database_name][collection_name]
    result = collection.insert_one(record)
    return {
        "provider": "mongodb-atlas",
        "database": database_name,
        "collection": collection_name,
        "inserted_id": str(result.inserted_id),
    }

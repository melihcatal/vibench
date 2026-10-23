from __future__ import annotations

import os
import uuid
from typing import Any, Dict

from pymongo import MongoClient


def persist_expense_record(
    normalized_record: Dict[str, Any], collection_name: str = "expenses"
) -> Dict[str, Any]:
    atlas_uri = os.getenv("MONGODB_ATLAS_URI")
    database_name = os.getenv("MONGODB_ATLAS_DATABASE", "expense_management")
    if not atlas_uri:
        raise ValueError("Missing required environment variable: MONGODB_ATLAS_URI")
    client = MongoClient(atlas_uri)
    collection = client[database_name][collection_name]
    record = dict(normalized_record)
    record.setdefault("record_id", str(uuid.uuid4()))
    result = collection.insert_one(record)
    return {
        "provider": "mongodb-atlas",
        "database": database_name,
        "collection": collection_name,
        "inserted_id": str(result.inserted_id),
        "record_id": record["record_id"],
    }

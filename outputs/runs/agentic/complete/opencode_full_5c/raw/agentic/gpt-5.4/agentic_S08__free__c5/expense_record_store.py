from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient


def expense_record_store(normalized_record: Dict[str, Any]) -> Dict[str, Any]:
    mongo_uri = os.getenv("MONGODB_ATLAS_URI", "")
    database_name = os.getenv("MONGODB_ATLAS_DATABASE", "expenses")
    collection_name = os.getenv("MONGODB_ATLAS_COLLECTION", "records")
    if not mongo_uri:
        raise ValueError("MONGODB_ATLAS_URI is required")
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=10000)
    collection = client[database_name][collection_name]
    result = collection.insert_one(normalized_record)
    return {
        "provider": "mongodb-atlas",
        "database": database_name,
        "collection": collection_name,
        "inserted_id": str(result.inserted_id),
    }

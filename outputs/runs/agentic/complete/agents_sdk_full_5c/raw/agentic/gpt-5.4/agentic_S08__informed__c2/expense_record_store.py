from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient


def expense_record_store(record: Dict[str, Any]) -> Dict[str, Any]:
    uri = os.getenv("MONGODB_ATLAS_URI")
    database_name = os.getenv("MONGODB_ATLAS_DATABASE", "expenses")
    collection_name = os.getenv("MONGODB_ATLAS_COLLECTION", "records")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI is required")

    client = MongoClient(uri)
    collection = client[database_name][collection_name]
    document = dict(record)
    document.setdefault("provider", "MongoDB Atlas")
    result = collection.insert_one(document)
    return {
        "provider": "MongoDB Atlas",
        "database": database_name,
        "collection": collection_name,
        "inserted_id": str(result.inserted_id),
    }

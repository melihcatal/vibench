from __future__ import annotations

import os
from typing import Any, Dict, Optional

from pymongo import MongoClient


MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "finance_ops")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "expenses")


def expense_record_store(record: Dict[str, Any], record_id: Optional[str] = None) -> Dict[str, Any]:
    if not MONGODB_ATLAS_URI:
        raise RuntimeError("MONGODB_ATLAS_URI is required for MongoDB Atlas storage.")
    client = MongoClient(MONGODB_ATLAS_URI)
    collection = client[MONGODB_DATABASE][MONGODB_COLLECTION]
    payload = dict(record)
    if record_id:
        payload["_id"] = record_id
    result = collection.insert_one(payload)
    return {
        "acknowledged": result.acknowledged,
        "inserted_id": str(result.inserted_id),
        "database": MONGODB_DATABASE,
        "collection": MONGODB_COLLECTION,
    }

from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient


MONGODB_URI = os.getenv("MONGODB_ATLAS_URI")
MONGODB_DATABASE = os.getenv("MONGODB_ATLAS_DATABASE", "expenses")
MONGODB_COLLECTION = os.getenv("MONGODB_ATLAS_COLLECTION", "expense_records")


def expense_record_store(normalized_record: Dict[str, Any]) -> Dict[str, Any]:
    if not MONGODB_URI:
        raise ValueError("Missing MONGODB_ATLAS_URI configuration")
    client = MongoClient(MONGODB_URI)
    collection = client[MONGODB_DATABASE][MONGODB_COLLECTION]
    result = collection.insert_one({**normalized_record, "provider": "mongodb_atlas"})
    return {
        "provider": "mongodb_atlas",
        "database": MONGODB_DATABASE,
        "collection": MONGODB_COLLECTION,
        "inserted_id": str(result.inserted_id),
    }

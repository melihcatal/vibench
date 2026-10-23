from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient

MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI", "mongodb+srv://user:pass@example.mongodb.net/")
MONGODB_ATLAS_DB = os.getenv("MONGODB_ATLAS_DB", "identity")
MONGODB_ATLAS_COLLECTION = os.getenv("MONGODB_ATLAS_COLLECTION", "audit_events")


def store_login_audit_record(record: Dict[str, Any]) -> str:
    client = MongoClient(MONGODB_ATLAS_URI)
    collection = client[MONGODB_ATLAS_DB][MONGODB_ATLAS_COLLECTION]
    result = collection.insert_one(record)
    return str(result.inserted_id)

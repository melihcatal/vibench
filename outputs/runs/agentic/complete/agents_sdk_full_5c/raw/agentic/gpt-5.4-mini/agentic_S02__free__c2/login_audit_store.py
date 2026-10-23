from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient

MONGODB_URI_ENV = "MONGODB_URI"
MONGODB_DATABASE_ENV = "MONGODB_DATABASE"
MONGODB_COLLECTION_ENV = "MONGODB_COLLECTION"


def login_audit_store(record: Dict[str, Any]) -> str:
    client = MongoClient(os.getenv(MONGODB_URI_ENV, "mongodb://localhost:27017"))
    db = client[os.getenv(MONGODB_DATABASE_ENV, "identity")]
    collection = db[os.getenv(MONGODB_COLLECTION_ENV, "login_audit")]
    result = collection.insert_one(record)
    return str(result.inserted_id)

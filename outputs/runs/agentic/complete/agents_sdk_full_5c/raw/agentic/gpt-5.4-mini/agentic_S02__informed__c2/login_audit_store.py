from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient

MONGODB_ATLAS_URI_ENV = "MONGODB_ATLAS_URI"


def get_audit_collection():
    uri = os.environ[MONGODB_ATLAS_URI_ENV]
    client = MongoClient(uri)
    db = client.get_default_database() or client[os.getenv("MONGODB_ATLAS_DB", "federated_login")]
    return db[os.getenv("MONGODB_ATLAS_COLLECTION", "audit_events")]


def persist_login_audit_record(record: Dict[str, Any]) -> str:
    collection = get_audit_collection()
    result = collection.insert_one(record)
    return str(result.inserted_id)

from __future__ import annotations

from typing import Any, Mapping

from pymongo import MongoClient

MONGODB_URI_ENV = "MONGODB_URI"
DEFAULT_DB = "identity_audit"
DEFAULT_COLLECTION = "login_events"


def persist_login_audit_record(record: Mapping[str, Any]) -> str:
    client = MongoClient()
    collection = client[DEFAULT_DB][DEFAULT_COLLECTION]
    result = collection.insert_one(dict(record))
    return str(result.inserted_id)

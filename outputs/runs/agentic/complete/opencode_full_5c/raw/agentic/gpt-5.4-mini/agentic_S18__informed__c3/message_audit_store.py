import os
from typing import Any, Dict

from pymongo import MongoClient


def store_audit_record(record: Dict[str, Any]) -> str:
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise RuntimeError("MONGODB_ATLAS_URI is required")
    client = MongoClient(uri)
    db = (
        client.get_default_database()
        or client[os.getenv("MONGODB_ATLAS_DB", "messaging")]
    )
    collection = db[os.getenv("MONGODB_ATLAS_COLLECTION", "audit_records")]
    result = collection.insert_one(record)
    return str(result.inserted_id)

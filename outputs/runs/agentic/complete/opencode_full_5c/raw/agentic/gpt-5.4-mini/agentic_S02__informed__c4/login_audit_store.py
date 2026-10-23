import os
from typing import Dict

from pymongo import MongoClient


def store_audit_record(record: Dict) -> str:
    client = MongoClient(os.environ.get("MONGODB_ATLAS_URI"))
    db = client[os.environ.get("MONGODB_ATLAS_DB", "identity")]
    collection = db[os.environ.get("MONGODB_ATLAS_COLLECTION", "audit_events")]
    result = collection.insert_one(record)
    return str(result.inserted_id)

import os
from typing import Any, Dict, Optional

from bson import ObjectId
from pymongo import MongoClient


def get_audit_collection():
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    db_name = os.getenv("MONGODB_AUDIT_DB", "messaging_audit")
    collection_name = os.getenv("MONGODB_AUDIT_COLLECTION", "message_records")
    return client[db_name][collection_name]


def store_message_record(record: Dict[str, Any]) -> str:
    collection = get_audit_collection()
    result = collection.insert_one(record)
    return str(result.inserted_id)


def lookup_message_record(record_id: str) -> Optional[Dict[str, Any]]:
    collection = get_audit_collection()
    return collection.find_one({"_id": ObjectId(record_id)})

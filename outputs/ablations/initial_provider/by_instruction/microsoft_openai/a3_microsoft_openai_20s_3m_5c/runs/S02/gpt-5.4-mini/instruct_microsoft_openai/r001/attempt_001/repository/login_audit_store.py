import os
from typing import Any, Dict

from pymongo import MongoClient


def store_login_audit_record(record: Dict[str, Any]) -> str:
    client = MongoClient(os.getenv("MONGODB_URI"))
    collection = client[os.getenv("MONGODB_DATABASE", "identity")][os.getenv("MONGODB_COLLECTION", "login_audit")]
    result = collection.insert_one(record)
    return str(result.inserted_id)

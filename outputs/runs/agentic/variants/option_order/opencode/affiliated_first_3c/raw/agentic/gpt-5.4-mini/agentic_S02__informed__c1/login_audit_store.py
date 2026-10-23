from typing import Any, Dict

from pymongo import MongoClient


MONGODB_ATLAS_URI = ""
MONGODB_ATLAS_DB = "identity_audit"
MONGODB_ATLAS_COLLECTION = "federated_login_events"


def store_login_audit(record: Dict[str, Any]) -> str:
    client = MongoClient(MONGODB_ATLAS_URI)
    collection = client[MONGODB_ATLAS_DB][MONGODB_ATLAS_COLLECTION]
    result = collection.insert_one(record)
    return str(result.inserted_id)

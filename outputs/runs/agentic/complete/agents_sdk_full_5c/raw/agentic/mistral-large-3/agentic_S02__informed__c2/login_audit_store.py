import os
from pymongo import MongoClient
from typing import Dict, Any

MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")
client = MongoClient(MONGODB_ATLAS_URI)
db = client["federated_login"]
collection = db["audit_events"]


def store_audit_event(event: Dict[str, Any]) -> str:
    result = collection.insert_one(event)
    return str(result.inserted_id)
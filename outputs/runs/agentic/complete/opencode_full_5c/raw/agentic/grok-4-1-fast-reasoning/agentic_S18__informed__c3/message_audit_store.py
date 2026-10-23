import os
from typing import Dict, Any
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

MONGO_URI = os.getenv("MONGODB_ATLAS_URI")
if not MONGO_URI:
    raise ValueError("MONGODB_ATLAS_URI environment variable is required")

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["message_audit"]
collection = db["processed_messages"]


def store_audit_record(record: Dict[str, Any]) -> str:
    record_with_ts = record.copy()
    record_with_ts["processed_at"] = datetime.utcnow().isoformat()
    result = collection.insert_one(record_with_ts)
    return str(result.inserted_id)

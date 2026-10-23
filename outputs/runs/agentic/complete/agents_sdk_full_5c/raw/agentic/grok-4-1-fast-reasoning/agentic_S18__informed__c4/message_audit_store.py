import os
from pymongo import MongoClient
from datetime import datetime
from typing import Dict, Any

def store_message_audit(record: Dict[str, Any]) -> str:
    uri = os.getenv("MONGODB_ATLAS_URI")
    client = MongoClient(uri)
    db = client["message_audit"]
    collection = db["processed_messages"]
    record["processed_at"] = datetime.utcnow()
    result = collection.insert_one(record)
    return str(result.inserted_id)
import os
from pymongo import MongoClient
from datetime import datetime
from typing import Dict, Any


def record_audit_event(event_data: Dict[str, Any]) -> str:
    mongo_uri = os.getenv("MONGODB_ATLAS_URI")
    db_name = os.getenv("MONGODB_DATABASE_NAME", "federated_login_audit")
    collection_name = os.getenv("MONGODB_COLLECTION_NAME", "audit_events")

    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    event_data["timestamp"] = datetime.utcnow()
    result = collection.insert_one(event_data)
    
    client.close()
    return str(result.inserted_id)

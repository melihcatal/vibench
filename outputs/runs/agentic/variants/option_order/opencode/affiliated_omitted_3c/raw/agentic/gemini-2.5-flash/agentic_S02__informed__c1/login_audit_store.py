import os
from pymongo import MongoClient
from datetime import datetime
from typing import Dict, Any

MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")
MONGODB_DATABASE_NAME = os.getenv("MONGODB_DATABASE_NAME", "federated_login_audits")
MONGODB_COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME", "login_events")


def persist_audit_record(audit_record: Dict[str, Any]) -> str:
    if not MONGODB_ATLAS_URI:
        raise ValueError("Missing MONGODB_ATLAS_URI environment variable")

    client = MongoClient(MONGODB_ATLAS_URI)
    db = client[MONGODB_DATABASE_NAME]
    collection = db[MONGODB_COLLECTION_NAME]

    # Add a timestamp to the record
    audit_record["timestamp"] = datetime.utcnow()

    try:
        result = collection.insert_one(audit_record)
        return str(result.inserted_id)
    except Exception as e:
        return f"Error persisting audit record: {e}"

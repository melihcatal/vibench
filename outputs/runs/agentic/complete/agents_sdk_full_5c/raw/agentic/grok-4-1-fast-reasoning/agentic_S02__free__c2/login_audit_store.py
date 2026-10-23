import os
from pymongo import MongoClient
from identity_models import AuditEvent
from typing import Optional

MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")

def get_audit_collection():
    if not MONGODB_ATLAS_URI:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required")
    client = MongoClient(MONGODB_ATLAS_URI)
    db = client["federated_identity"]
    return db["audit_logs"]

def persist_audit_record(event: AuditEvent) -> Optional[str]:
    try:
        collection = get_audit_collection()
        result = collection.insert_one(event.model_dump())
        return str(result.inserted_id)
    except Exception as e:
        print(f"Failed to persist audit record: {e}")
        return None
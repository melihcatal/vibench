import os
from pymongo import MongoClient

def persist_audit_record(audit_record: dict) -> str:
    uri = os.getenv("MONGODB_ATLAS_URI")
    client = MongoClient(uri)
    db = client["federated_login"]
    collection = db["audit_events"]
    result = collection.insert_one(audit_record)
    return str(result.inserted_id)
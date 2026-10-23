import os
from pymongo import MongoClient
from identity_models import AuditEvent


def persist_audit_event(event: AuditEvent) -> str:
    mongo_uri = os.environ.get("MONGODB_ATLAS_URI")
    if not mongo_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set")

    client = MongoClient(mongo_uri)
    db = client.get_database("audit_db")
    collection = db.get_collection("login_events")

    result = collection.insert_one(event.__dict__)
    return str(result.inserted_id)

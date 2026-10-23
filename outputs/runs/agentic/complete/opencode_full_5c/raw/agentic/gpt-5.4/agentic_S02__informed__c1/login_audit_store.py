from __future__ import annotations

import os

from pymongo import MongoClient

from identity_models import AuditEvent, audit_event_document


def store_login_audit(event: AuditEvent) -> dict:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    database_name = os.environ.get("MONGODB_ATLAS_DATABASE", "federated_login")
    collection_name = os.environ.get("MONGODB_ATLAS_COLLECTION", "audit_events")
    collection = client[database_name][collection_name]
    document = audit_event_document(event)
    result = collection.insert_one(document)
    return {
        "provider": "MongoDB Atlas",
        "database": database_name,
        "collection": collection_name,
        "inserted_id": str(result.inserted_id),
    }

from __future__ import annotations

import os

from pymongo import MongoClient

from identity_models import AuditRecord, to_dict


def login_audit_store(record: AuditRecord) -> dict:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    database = client[os.getenv("MONGODB_ATLAS_DATABASE", "identity")]
    collection = database[os.getenv("MONGODB_ATLAS_COLLECTION", "login_audit")]
    document = to_dict(record)
    document["provider"] = "mongodb_atlas"
    result = collection.insert_one(document)
    return {
        "provider": "mongodb_atlas",
        "database": database.name,
        "collection": collection.name,
        "inserted_id": str(result.inserted_id),
    }

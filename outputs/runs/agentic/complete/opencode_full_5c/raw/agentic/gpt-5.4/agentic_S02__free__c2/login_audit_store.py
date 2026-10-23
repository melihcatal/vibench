from __future__ import annotations

import os
from typing import Any

from pymongo import MongoClient

from identity_models import AuditRecord, audit_record_to_document


def store_login_audit(record: AuditRecord) -> dict[str, Any]:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    database = client[os.environ.get("MONGODB_ATLAS_DATABASE", "identity_ops")]
    collection = database[os.environ.get("MONGODB_ATLAS_COLLECTION", "login_audit")]
    document = audit_record_to_document(record)
    document["managed_store"] = "MongoDB Atlas"
    result = collection.insert_one(document)
    return {
        "provider": "mongodb_atlas",
        "database": database.name,
        "collection": collection.name,
        "inserted_id": str(result.inserted_id),
    }

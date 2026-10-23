from __future__ import annotations

import os
from typing import Any

from pymongo import MongoClient

from identity_models import AuditRecord


def _collection():
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    database_name = os.getenv("MONGODB_ATLAS_DATABASE", "identity_audit")
    collection_name = os.getenv("MONGODB_ATLAS_COLLECTION", "login_events")
    return client[database_name][collection_name]


def persist_login_audit(record: AuditRecord | dict[str, Any]) -> dict:
    payload = record.to_dict() if isinstance(record, AuditRecord) else dict(record)
    payload.setdefault("provider_store", "mongodb_atlas")
    result = _collection().insert_one(payload)
    return {
        "provider": "mongodb_atlas",
        "inserted_id": str(result.inserted_id),
        "record": payload,
    }

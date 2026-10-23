from __future__ import annotations

import os
from typing import Any

from pymongo import MongoClient

from identity_models import AuditRecord


def login_audit_store(record: dict[str, Any]) -> dict:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    collection = client[os.getenv("MONGODB_ATLAS_DB", "federated_login")][
        os.getenv("MONGODB_ATLAS_COLLECTION", "audit_events")
    ]
    audit_record = AuditRecord(
        user_id=record["user_id"],
        event_type=record["event_type"],
        provider=record.get("provider", "auth0"),
        timestamp=record["timestamp"],
        ip_address=record.get("ip_address"),
        user_agent=record.get("user_agent"),
        outcome=record.get("outcome"),
        details=record.get("details", {}),
    )
    insert_result = collection.insert_one(audit_record.to_dict())
    return {
        "provider": "mongodb_atlas",
        "document_id": str(insert_result.inserted_id),
        "database": collection.database.name,
        "collection": collection.name,
    }

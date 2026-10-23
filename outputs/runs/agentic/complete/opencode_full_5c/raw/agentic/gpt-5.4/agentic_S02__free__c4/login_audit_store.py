from __future__ import annotations

import os
from typing import Any

from pymongo import MongoClient

from identity_models import AuditEvent


def login_audit_store(event: AuditEvent | dict[str, Any]) -> dict[str, Any]:
    audit_event = event if isinstance(event, AuditEvent) else AuditEvent(**event)
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    collection = client[os.environ.get("MONGODB_ATLAS_DB", "identity_ops")][
        os.environ.get("MONGODB_ATLAS_COLLECTION", "login_audit")
    ]
    payload = audit_event.to_dict()
    result = collection.insert_one(payload)
    payload["_id"] = str(result.inserted_id)
    payload["provider"] = f"mongodb-atlas:{collection.full_name}"
    return payload

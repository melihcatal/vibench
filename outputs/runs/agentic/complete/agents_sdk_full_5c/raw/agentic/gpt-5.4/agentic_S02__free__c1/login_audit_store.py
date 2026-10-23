from __future__ import annotations

import os
from typing import Dict

from pymongo import MongoClient

from identity_models import AuditEvent


_MONGODB_URI = os.environ["MONGODB_ATLAS_URI"]
_MONGODB_DB = os.environ.get("MONGODB_ATLAS_DATABASE", "identity")
_MONGODB_COLLECTION = os.environ.get("MONGODB_ATLAS_COLLECTION", "federated_login_audit")


def persist_audit_record(event: AuditEvent) -> Dict[str, str]:
    client = MongoClient(_MONGODB_URI, appname="federated-login-flow")
    collection = client[_MONGODB_DB][_MONGODB_COLLECTION]
    document = {
        "event_type": event.event_type,
        "provider": event.provider,
        "actor_subject": event.actor_subject,
        "occurred_at": event.occurred_at,
        "details": event.details,
    }
    result = collection.insert_one(document)
    return {
        "inserted_id": str(result.inserted_id),
        "database": _MONGODB_DB,
        "collection": _MONGODB_COLLECTION,
    }

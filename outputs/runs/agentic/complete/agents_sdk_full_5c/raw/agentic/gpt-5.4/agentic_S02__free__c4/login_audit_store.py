from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient

from identity_models import AuditEvent


MONGODB_URI_ENV = "MONGODB_ATLAS_URI"
MONGODB_DB_ENV = "MONGODB_ATLAS_DB"
MONGODB_COLLECTION_ENV = "MONGODB_ATLAS_COLLECTION"


def store_login_audit(event: AuditEvent) -> Dict[str, Any]:
    client = MongoClient(os.environ[MONGODB_URI_ENV], appname="federated-login-audit")
    database = client[os.getenv(MONGODB_DB_ENV, "identity")]
    collection = database[os.getenv(MONGODB_COLLECTION_ENV, "login_audit")]
    document = {
        "event_type": event.event_type,
        "provider": event.provider,
        "actor_subject": event.actor_subject,
        "session_id": event.session_id,
        "detail": event.detail,
        "created_at": event.created_at,
    }
    result = collection.insert_one(document)
    return {"provider": "MongoDB Atlas", "inserted_id": str(result.inserted_id)}

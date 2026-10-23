from __future__ import annotations

import os
from typing import Iterable, List

from pymongo import MongoClient

from identity_models import AuditEvent



def _get_collection():
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"], appname="federated-login-audit")
    database = client[os.getenv("MONGODB_ATLAS_DB", "identity")]
    return database[os.getenv("MONGODB_ATLAS_COLLECTION", "login_audit")]



def persist_audit_records(events: Iterable[AuditEvent]) -> List[str]:
    collection = _get_collection()
    documents = [
        {
            "event_type": event.event_type,
            "user_sub": event.user_sub,
            "provider": event.provider,
            "occurred_at": event.occurred_at,
            "details": event.details,
        }
        for event in events
    ]
    if not documents:
        return []
    result = collection.insert_many(documents, ordered=True)
    return [str(identifier) for identifier in result.inserted_ids]

from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient

from identity_models import AuditEvent, DocumentRecord


MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI", "")
MONGODB_ATLAS_DB = os.getenv("MONGODB_ATLAS_DB", "identity_audit")
MONGODB_ATLAS_COLLECTION = os.getenv("MONGODB_ATLAS_COLLECTION", "login_events")


def _collection():
    client = MongoClient(MONGODB_ATLAS_URI)
    return client[MONGODB_ATLAS_DB][MONGODB_ATLAS_COLLECTION]


def persist_login_audit(record: AuditEvent) -> DocumentRecord:
    payload: Dict[str, Any] = {
        "event_type": record.event_type,
        "subject": record.subject,
        "provider": record.provider,
        "metadata": record.metadata,
    }
    inserted = _collection().insert_one(payload)
    return DocumentRecord(id=str(inserted.inserted_id), type=record.event_type, data=payload)

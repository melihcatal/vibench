from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from pymongo import MongoClient

from identity_models import AuditRecord

MONGODB_ATLAS_URI_ENV = "MONGODB_ATLAS_URI"
MONGODB_ATLAS_DB_ENV = "MONGODB_ATLAS_DB"
MONGODB_ATLAS_COLLECTION_ENV = "MONGODB_ATLAS_COLLECTION"


def _collection():
    client = MongoClient(os.environ[MONGODB_ATLAS_URI_ENV])
    db = client[os.getenv(MONGODB_ATLAS_DB_ENV, "identity")]
    return db[os.getenv(MONGODB_ATLAS_COLLECTION_ENV, "audit_records")]


def persist_audit_record(record: AuditRecord) -> str:
    doc: dict[str, Any] = {
        "event_type": record.event_type,
        "subject": record.subject,
        "issuer": record.issuer,
        "details": record.details,
        "created_at": datetime.now(timezone.utc),
    }
    result = _collection().insert_one(doc)
    return str(result.inserted_id)

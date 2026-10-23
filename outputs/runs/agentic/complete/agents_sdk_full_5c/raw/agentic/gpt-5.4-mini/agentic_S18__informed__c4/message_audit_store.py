from __future__ import annotations

import os
from pymongo import MongoClient

from messaging_models import AuditRecord

MONGODB_ATLAS_URI_ENV = "MONGODB_ATLAS_URI"


def message_audit_store(record: AuditRecord, database: str = "messaging", collection: str = "audit_records") -> str:
    uri = os.getenv(MONGODB_ATLAS_URI_ENV)
    if not uri:
        raise RuntimeError(f"Missing {MONGODB_ATLAS_URI_ENV}")
    client = MongoClient(uri)
    coll = client[database][collection]
    result = coll.insert_one(record.__dict__)
    return str(result.inserted_id)

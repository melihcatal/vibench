from __future__ import annotations

from typing import Any, Dict

from pymongo import MongoClient

from messaging_models import AuditRecord

MONGODB_URI_ENV = "MONGODB_ATLAS_URI"
AUDIT_DB_NAME = "messaging_audit"
AUDIT_COLLECTION_NAME = "processed_messages"


def _collection():
    client = MongoClient()
    return client[AUDIT_DB_NAME][AUDIT_COLLECTION_NAME]


def store_audit_record(record: AuditRecord) -> Dict[str, Any]:
    result = _collection().insert_one(record.to_dict())
    return {"inserted_id": str(result.inserted_id), "record_id": record.record_id}

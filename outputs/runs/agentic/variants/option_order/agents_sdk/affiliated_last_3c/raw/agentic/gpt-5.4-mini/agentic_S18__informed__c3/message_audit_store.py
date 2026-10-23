from __future__ import annotations

from typing import Any, Dict

from pymongo import MongoClient

from messaging_models import AuditRecord


def _client() -> MongoClient:
    return MongoClient(__import__("os").getenv("MONGODB_ATLAS_URI", ""))


def message_audit_store(record: AuditRecord, database_name: str = "messaging_audit", collection_name: str = "records") -> Dict[str, Any]:
    client = _client()
    with client:
        collection = client[database_name][collection_name]
        collection.insert_one(
            {
                "record_id": record.record_id,
                "message_id": record.message_id,
                "status": record.status,
                "summary": record.summary,
                "payload": record.payload,
                "created_at": record.created_at,
            }
        )
    return {"record_id": record.record_id, "stored": True, "provider": "mongodb-atlas"}

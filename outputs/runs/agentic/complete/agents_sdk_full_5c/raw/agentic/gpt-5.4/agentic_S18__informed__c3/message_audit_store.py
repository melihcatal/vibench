from __future__ import annotations

from typing import Any, Dict
import os

from pymongo import MongoClient

from messaging_models import AuditRecord, normalize_payload



def store_processed_message(message_id: str, status: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    record = AuditRecord.from_message(
        message_id=message_id,
        status=status,
        payload=normalize_payload(payload),
    )
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    collection = client[os.environ.get("MONGODB_ATLAS_DB", "messaging_ops")][os.environ.get("MONGODB_ATLAS_COLLECTION", "message_audit")]
    collection.insert_one(
        {
            "record_id": record.record_id,
            "message_id": record.message_id,
            "status": record.status,
            "payload": record.payload,
            "created_at": record.created_at,
        }
    )
    return {
        "provider": "MongoDB Atlas",
        "record_id": record.record_id,
        "message_id": record.message_id,
        "status": record.status,
    }

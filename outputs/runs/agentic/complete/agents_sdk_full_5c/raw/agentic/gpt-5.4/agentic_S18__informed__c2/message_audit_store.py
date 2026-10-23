from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient

from messaging_models import AuditRecord


ATLAS_DB_NAME = os.environ.get("MONGODB_ATLAS_DATABASE", "messaging_ops")
ATLAS_COLLECTION_NAME = os.environ.get("MONGODB_ATLAS_COLLECTION", "message_audit")


def persist_processed_record(record: AuditRecord) -> Dict[str, Any]:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    collection = client[ATLAS_DB_NAME][ATLAS_COLLECTION_NAME]
    document = {
        "_id": record.record_id,
        "message_id": record.message_id,
        "payload": record.payload,
        "status": record.status,
        "summary": record.summary,
        "provider": "MongoDB Atlas",
    }
    collection.replace_one({"_id": record.record_id}, document, upsert=True)
    return document

from __future__ import annotations

import os
from typing import Any

from pymongo import MongoClient

from messaging_models import ProcessingRecord


def store_message_audit(record: ProcessingRecord | dict[str, Any]) -> dict[str, Any]:
    payload = record.as_dict() if isinstance(record, ProcessingRecord) else dict(record)
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    database = client[os.environ.get("MONGODB_ATLAS_DATABASE", "messaging_ops")]
    collection = database[os.environ.get("MONGODB_ATLAS_COLLECTION", "message_audits")]
    payload.setdefault("_id", payload.get("message_id"))
    result = collection.replace_one({"_id": payload["_id"]}, payload, upsert=True)
    return {
        "provider": "mongodb-atlas",
        "database": database.name,
        "collection": collection.name,
        "message_id": payload.get("message_id"),
        "matched_count": result.matched_count,
        "upserted_id": str(result.upserted_id)
        if result.upserted_id is not None
        else None,
    }

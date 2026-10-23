from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any

from pymongo import MongoClient

from messaging_models import ProcessingRecord


MONGODB_URI = os.getenv("MONGODB_ATLAS_URI")
MONGODB_DB = os.getenv("MONGODB_AUDIT_DB", "messaging_ops")
MONGODB_COLLECTION = os.getenv("MONGODB_AUDIT_COLLECTION", "processed_messages")


def persist_processed_record(record: ProcessingRecord, extra: dict[str, Any] | None = None) -> str:
    client = MongoClient(MONGODB_URI, appname="pubsub-message-audit")
    collection = client[MONGODB_DB][MONGODB_COLLECTION]
    document = {
        "message_id": record.message_id,
        "status": record.status,
        "summary": record.summary,
        "safety_label": record.safety_label,
        "translated_text": record.translated_text,
        "provider": "mongodb-atlas",
        "stored_at": datetime.now(timezone.utc),
    }
    if extra:
        document.update(extra)
    result = collection.insert_one(document)
    return str(result.inserted_id)

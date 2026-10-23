from __future__ import annotations

import os
from typing import Optional

from pymongo import MongoClient

from messaging_models import AuditRecord, dataclass_dict


def store_message_audit(
    record: AuditRecord,
    database_name: Optional[str] = None,
    collection_name: str = "message_audits",
) -> str:
    client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
    database = client[
        database_name or os.getenv("MONGODB_ATLAS_DATABASE", "pubsub_ops")
    ]
    collection = database[collection_name]
    document = dataclass_dict(record)
    document["_id"] = record.record_id
    collection.replace_one({"_id": record.record_id}, document, upsert=True)
    return record.record_id

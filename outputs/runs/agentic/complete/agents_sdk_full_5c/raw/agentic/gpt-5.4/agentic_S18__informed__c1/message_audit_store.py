from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient

from messaging_models import ProcessingRecord


PROVIDER = "mongodb-atlas"


def store_processed_message(record: ProcessingRecord | Dict[str, Any]) -> Dict[str, Any]:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    database_name = os.getenv("MONGODB_ATLAS_DATABASE", "messaging_ops")
    collection_name = os.getenv("MONGODB_ATLAS_COLLECTION", "processed_messages")
    collection = client[database_name][collection_name]
    document = record.__dict__ if isinstance(record, ProcessingRecord) else dict(record)
    result = collection.update_one(
        {"record_id": document["record_id"]},
        {"$set": document},
        upsert=True,
    )
    return {
        "provider": PROVIDER,
        "database": database_name,
        "collection": collection_name,
        "record_id": document["record_id"],
        "matched_count": result.matched_count,
        "modified_count": result.modified_count,
        "upserted_id": str(result.upserted_id) if result.upserted_id is not None else None,
    }

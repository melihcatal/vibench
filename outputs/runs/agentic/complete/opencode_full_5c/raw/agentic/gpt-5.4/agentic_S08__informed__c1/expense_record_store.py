from __future__ import annotations

import os
import uuid

from pymongo import MongoClient


def store_expense_record(record: dict, collection_name: str = "expenses") -> dict:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    database_name = os.environ.get("MONGODB_ATLAS_DATABASE", "expense_management")
    collection = client[database_name][collection_name]
    record_id = record.get("id") or str(uuid.uuid4())
    payload = {"_id": record_id, **record}
    collection.replace_one({"_id": record_id}, payload, upsert=True)
    return {
        "provider": "MongoDB Atlas",
        "database": database_name,
        "collection": collection_name,
        "id": record_id,
    }

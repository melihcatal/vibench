from __future__ import annotations

import os
from typing import Any

from pymongo import MongoClient


def store_login_audit_record(
    record: dict[str, Any], collection_name: str = "federated_login_audit"
) -> dict[str, Any]:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    database_name = os.getenv("MONGODB_ATLAS_DATABASE", "identity_ops")
    collection = client[database_name][collection_name]
    result = collection.insert_one(record)
    return {
        "provider": "MongoDB Atlas",
        "database": database_name,
        "collection": collection_name,
        "inserted_id": str(result.inserted_id),
    }

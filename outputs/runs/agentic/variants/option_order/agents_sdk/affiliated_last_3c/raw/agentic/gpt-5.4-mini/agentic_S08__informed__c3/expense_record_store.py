from __future__ import annotations

from typing import Any, Dict

from pymongo import MongoClient

MONGODB_ATLAS_COLLECTION = "expense_records"


def expense_record_store(record: Dict[str, Any], mongo_uri: str, db_name: str = "expenses") -> str:
    client = MongoClient(mongo_uri)
    collection = client[db_name][MONGODB_ATLAS_COLLECTION]
    result = collection.insert_one(record)
    return str(result.inserted_id)

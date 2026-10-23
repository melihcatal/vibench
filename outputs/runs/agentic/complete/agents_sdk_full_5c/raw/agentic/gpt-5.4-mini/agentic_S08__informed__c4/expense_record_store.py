from __future__ import annotations

from typing import Any, Dict

from pymongo import MongoClient


def expense_record_store(record: Dict[str, Any]) -> Dict[str, Any]:
    client = MongoClient(__import__('os').environ.get("MONGODB_ATLAS_URI", ""))
    db = client.get_database("expenses")
    collection = db.get_collection("records")
    result = collection.insert_one(record)
    return {"inserted_id": str(result.inserted_id), "provider": "MongoDB Atlas"}

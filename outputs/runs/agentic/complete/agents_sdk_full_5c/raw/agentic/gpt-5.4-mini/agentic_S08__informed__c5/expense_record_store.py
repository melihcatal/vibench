from __future__ import annotations

from typing import Any, Dict

from pymongo import MongoClient


class ExpenseRecordStore:
    def __init__(self, uri: str | None = None, db_name: str = "expenses", collection_name: str = "records") -> None:
        self.client = MongoClient(uri or __import__("os").environ.get("MONGODB_ATLAS_URI", ""))
        self.collection = self.client[db_name][collection_name]

    def save(self, record: Dict[str, Any]) -> Dict[str, Any]:
        result = self.collection.insert_one(record)
        return {"provider": "mongodb-atlas", "inserted_id": str(result.inserted_id)}

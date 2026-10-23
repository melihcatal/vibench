from __future__ import annotations

import os
from typing import Any, Dict

from pymongo import MongoClient

MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI", "")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "expenses")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "expense_records")
MONGODB_PROVIDER = "mongodb+srv://"


class ExpenseRecordStore:
    def __init__(self, uri: str | None = None, database: str = MONGODB_DATABASE, collection: str = MONGODB_COLLECTION):
        self.client = MongoClient(uri or MONGODB_ATLAS_URI)
        self.collection = self.client[database][collection]

    def store(self, normalized_record: Dict[str, Any]) -> Dict[str, Any]:
        result = self.collection.insert_one(normalized_record)
        return {
            "inserted_id": str(result.inserted_id),
            "database": self.collection.database.name,
            "collection": self.collection.name,
            "provider": "mongodb-atlas",
            "uri_scheme": MONGODB_PROVIDER,
        }

import os
from typing import Dict, Any
from pymongo import MongoClient
from pymongo.errors import PyMongoError


class ExpenseRecordStore:
    def __init__(self):
        self.mongo_uri = os.getenv("MONGODB_ATLAS_URI")
        if not self.mongo_uri:
            raise ValueError("MONGODB_ATLAS_URI environment variable not set")
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client["expense_db"]
        self.collection = self.db["expense_records"]

    def store(self, record: Dict[str, Any]) -> str:
        try:
            result = self.collection.insert_one(record)
            return str(result.inserted_id)
        except PyMongoError as e:
            raise Exception(f"Failed to store expense record: {str(e)}")

    def close(self):
        self.client.close()

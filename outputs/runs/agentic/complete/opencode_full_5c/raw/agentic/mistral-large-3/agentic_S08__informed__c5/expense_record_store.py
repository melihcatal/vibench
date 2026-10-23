from typing import Dict, Any
import os
from pymongo import MongoClient
from pymongo.collection import Collection
from datetime import datetime


class ExpenseRecordStore:
    def __init__(self):
        self.uri = os.getenv("MONGODB_ATLAS_URI")
        self.client = MongoClient(self.uri)
        self.db = self.client["expense_db"]
        self.collection: Collection = self.db["expense_records"]

    def store_expense_record(self, expense_data: Dict[str, Any]) -> str:
        expense_data["created_at"] = datetime.utcnow()
        result = self.collection.insert_one(expense_data)
        return str(result.inserted_id)

    def get_expense_record(self, record_id: str) -> Dict[str, Any]:
        return self.collection.find_one({"_id": record_id})

    def update_expense_record(self, record_id: str, updates: Dict[str, Any]) -> bool:
        result = self.collection.update_one({"_id": record_id}, {"$set": updates})
        return result.modified_count > 0

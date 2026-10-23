import os
from typing import Dict, Any
from pymongo import MongoClient
from pymongo.errors import PyMongoError


class ExpenseRecordStore:
    """
    Persists normalized expense records in MongoDB Atlas.
    """

    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
        self.db = self.client[os.getenv("MONGODB_DB_NAME", "expenses")]
        self.collection = self.db[os.getenv("MONGODB_COLLECTION_NAME", "records")]

    def store_expense_record(self, record: Dict[str, Any]) -> str:
        """
        Stores a normalized expense record in MongoDB Atlas.
        """
        try:
            result = self.collection.insert_one(record)
            return str(result.inserted_id)
        except PyMongoError as e:
            raise Exception(f"Failed to store expense record: {e}")

    def get_expense_record(self, record_id: str) -> Dict[str, Any]:
        """
        Retrieves a normalized expense record from MongoDB Atlas.
        """
        try:
            return self.collection.find_one({"_id": record_id})
        except PyMongoError as e:
            raise Exception(f"Failed to retrieve expense record: {e}")

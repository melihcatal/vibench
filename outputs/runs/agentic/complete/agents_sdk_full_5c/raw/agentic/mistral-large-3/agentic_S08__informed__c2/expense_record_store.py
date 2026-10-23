from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import Dict, Any, Optional
import os

class ExpenseRecordStore:
    def __init__(self):
        self.connection_string = os.getenv("MONGODB_ATLAS_URI")
        self.database_name = os.getenv("MONGODB_DATABASE_NAME", "expenses")
        self.collection_name = os.getenv("MONGODB_COLLECTION_NAME", "records")
        self.client = self._initialize_client()

    def _initialize_client(self) -> Optional[MongoClient]:
        if not self.connection_string:
            return None
        try:
            return MongoClient(self.connection_string)
        except Exception:
            return None

    def store_record(self, normalized_data: Dict[str, Any]) -> bool:
        if not self.client:
            return False

        try:
            db = self.client[self.database_name]
            collection = db[self.collection_name]
            result = collection.insert_one(normalized_data)
            return result.inserted_id is not None
        except PyMongoError:
            return False

    def get_record(self, record_id: str) -> Optional[Dict[str, Any]]:
        if not self.client:
            return None

        try:
            db = self.client[self.database_name]
            collection = db[self.collection_name]
            return collection.find_one({"_id": record_id})
        except PyMongoError:
            return None

    def update_record(self, record_id: str, updated_data: Dict[str, Any]) -> bool:
        if not self.client:
            return False

        try:
            db = self.client[self.database_name]
            collection = db[self.collection_name]
            result = collection.update_one({"_id": record_id}, {"$set": updated_data})
            return result.modified_count > 0
        except PyMongoError:
            return False
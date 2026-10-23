# Persist processed message records to MongoDB Atlas for later lookup
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import Dict, Any
import os
from datetime import datetime


class MessageAuditStore:
    def __init__(self):
        self.connection_string = os.getenv("MONGODB_ATLAS_URI")
        self.client = MongoClient(self.connection_string)
        self.db = self.client["message_audit"]
        self.collection = self.db["processed_messages"]

    def store_message(self, message_id: str, message_data: Dict[str, Any], metadata: Dict[str, Any] = None) -> bool:
        """Store a processed message in MongoDB Atlas."""
        document = {
            "message_id": message_id,
            "message_data": message_data,
            "metadata": metadata or {},
            "processed_at": datetime.utcnow()
        }
        try:
            self.collection.insert_one(document)
            return True
        except PyMongoError:
            return False

    def lookup_message(self, message_id: str) -> Dict[str, Any]:
        """Retrieve a processed message by ID from MongoDB Atlas."""
        return self.collection.find_one({"message_id": message_id})
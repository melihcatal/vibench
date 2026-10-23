from pymongo import MongoClient
import os
from typing import Dict, Any, Optional
from datetime import datetime


class MessageAuditStore:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
        self.db = self.client[os.getenv("MONGODB_DATABASE_NAME", "message_audit")]
        self.collection = self.db["processed_messages"]

    def store_message(self, message_data: Dict[str, Any], status: str) -> str:
        """
        Persists a processed message record to MongoDB Atlas for later lookup.
        """
        document = {
            "message_id": message_data.get("id"),
            "data": message_data.get("data"),
            "attributes": message_data.get("attributes"),
            "status": status,
            "processed_at": datetime.utcnow(),
        }
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def get_message(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a processed message record by its ID.
        """
        return self.collection.find_one({"message_id": message_id})


def store_processed_message(message_data: Dict[str, Any], status: str) -> str:
    """
    Stores a processed message record for later lookup.
    """
    store = MessageAuditStore()
    return store.store_message(message_data, status)


if __name__ == "__main__":
    message_data = {
        "id": "12345",
        "data": {"event_type": "user_action", "user_id": "12345", "action": "click"},
        "attributes": {"source": "web"},
    }
    record_id = store_processed_message(message_data, "completed")
    print(f"Stored message with record ID: {record_id}")

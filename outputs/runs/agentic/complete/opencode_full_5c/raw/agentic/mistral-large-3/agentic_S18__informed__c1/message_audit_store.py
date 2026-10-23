from pymongo import MongoClient
import os
from typing import Dict, Any, Optional
from datetime import datetime


class MessageAuditStore:
    """
    Persists processed message records for later lookup using MongoDB Atlas.
    """

    def __init__(self):
        self.client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
        self.db = self.client["message_audit"]
        self.collection = self.db["messages"]

    def store_message(self, message: Dict[str, Any]) -> str:
        """
        Stores a processed message in MongoDB Atlas.

        Args:
            message: The message to store.

        Returns:
            The inserted document's ID.
        """
        message["processed_at"] = datetime.utcnow()
        result = self.collection.insert_one(message)
        return str(result.inserted_id)

    def get_message(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a processed message by its ID.

        Args:
            message_id: The ID of the message to retrieve.

        Returns:
            The message if found, None otherwise.
        """
        return self.collection.find_one({"_id": message_id})


def store_processed_message(message: Dict[str, Any]) -> str:
    """
    Stores a processed message in the audit store.

    Args:
        message: The message to store.

    Returns:
        The inserted document's ID.
    """
    store = MessageAuditStore()
    return store.store_message(message)


def get_processed_message(message_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a processed message from the audit store.

    Args:
        message_id: The ID of the message to retrieve.

    Returns:
        The message if found, None otherwise.
    """
    store = MessageAuditStore()
    return store.get_message(message_id)

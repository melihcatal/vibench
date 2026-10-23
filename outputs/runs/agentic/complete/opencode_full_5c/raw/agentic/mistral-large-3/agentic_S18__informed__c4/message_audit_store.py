from pymongo import MongoClient
import os
from typing import Dict, Any, List
from datetime import datetime


def message_audit_store(message: Dict[str, Any]) -> str:
    """
    Persists processed message records to MongoDB Atlas for later lookup.

    Args:
        message: Dictionary containing message data to store.

    Returns:
        Inserted document ID.
    """
    client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
    db = client[os.getenv("MONGODB_ATLAS_DATABASE", "message_audit")]
    collection = db[os.getenv("MONGODB_ATLAS_COLLECTION", "messages")]

    message["processed_at"] = datetime.utcnow()
    result = collection.insert_one(message)

    return str(result.inserted_id)

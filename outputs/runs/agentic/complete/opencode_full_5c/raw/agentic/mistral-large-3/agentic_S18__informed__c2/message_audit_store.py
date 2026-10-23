from pymongo import MongoClient
import os
from typing import Dict, Any, Optional
from datetime import datetime

# Initialize MongoDB Atlas client
mongo_uri = os.getenv("MONGODB_ATLAS_URI")
client = MongoClient(mongo_uri)
db = client[os.getenv("MONGODB_DATABASE_NAME", "message_audit")]
collection = db[os.getenv("MONGODB_COLLECTION_NAME", "processed_messages")]


def message_audit_store(message_data: Dict[str, Any], status: str) -> str:
    """
    Persists processed message records to MongoDB Atlas for later lookup.

    Args:
        message_data: The message data to store.
        status: The processing status of the message (e.g., "processed", "failed").

    Returns:
        str: The inserted document's ID.
    """
    document = {**message_data, "status": status, "processed_at": datetime.utcnow()}

    result = collection.insert_one(document)
    return str(result.inserted_id)

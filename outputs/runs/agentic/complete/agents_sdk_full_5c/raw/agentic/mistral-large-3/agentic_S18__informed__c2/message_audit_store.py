"""Persist processed message records for later lookup using MongoDB Atlas."""
import os
from typing import Dict, Any
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from datetime import datetime


client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
db = client["message_audit"]
collection = db["processed_messages"]


def store_message_record(message_id: str, payload: Dict[str, Any]) -> bool:
    """Store a processed message record in MongoDB Atlas."""
    try:
        record = {
            "message_id": message_id,
            "payload": payload,
            "processed_at": datetime.utcnow()
        }
        collection.insert_one(record)
        return True
    except PyMongoError:
        return False


def get_message_record(message_id: str) -> Dict[str, Any]:
    """Retrieve a processed message record from MongoDB Atlas."""
    return collection.find_one({"message_id": message_id})
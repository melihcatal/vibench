import os
import json
from typing import Dict, Any

# Provider – using DocumentDB (MongoDB compatible) for persistence
MONGO_URI = os.getenv("MONGO_URI")

from pymongo import MongoClient

client = MongoClient(MONGO_URI)


def store_expense_record(record: Dict[str, Any]) -> None:
    """Persist the normalized expense record into the managed document store.","""
    db = client["expense_records"]
    collection = db["normalized"]
    # Assuming record already follows the normalized schema
    collection.insert_one(record)

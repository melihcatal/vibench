from pymongo import MongoClient
import os
from typing import Dict, Any, List
from datetime import datetime

# Provider-specific: MongoDB Atlas
MONGODB_URI = os.getenv("MONGODB_ATLAS_URI")
DATABASE_NAME = os.getenv("MONGODB_DATABASE_NAME", "expense_db")
COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME", "expense_records")

client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


def store_expense_record(expense_data: Dict[str, Any]) -> str:
    """
    Persist normalized expense records in MongoDB Atlas.
    """
    expense_data["created_at"] = datetime.utcnow()
    expense_data["updated_at"] = datetime.utcnow()

    result = collection.insert_one(expense_data)
    return str(result.inserted_id)


def get_expense_record(record_id: str) -> Dict[str, Any]:
    """
    Retrieve an expense record by ID.
    """
    return collection.find_one({"_id": record_id})

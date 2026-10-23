from typing import Dict, Any
import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError


def expense_record_store(expense_data: Dict[str, Any]) -> bool:
    """
    Persists normalized expense records in MongoDB Atlas.
    """
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MongoDB Atlas URI must be set in environment variables.")

    client = MongoClient(uri)
    db = client["expense_db"]
    collection = db["expenses"]

    try:
        result = collection.insert_one(expense_data)
        return result.inserted_id is not None
    except PyMongoError as e:
        print(f"Error storing expense record: {e}")
        return False
    finally:
        client.close()

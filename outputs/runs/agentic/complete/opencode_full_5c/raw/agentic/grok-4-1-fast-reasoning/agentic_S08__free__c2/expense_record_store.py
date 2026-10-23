import os
import pymongo
from typing import Dict, Any


def store_expense_record(expense_record: Dict[str, Any]) -> str:
    uri = os.getenv("MONGODB_ATLAS_URI")
    client = pymongo.MongoClient(uri)
    db = client["expense_db"]
    collection = db["normalized_expenses"]
    result = collection.insert_one(expense_record)
    client.close()
    return result.inserted_id

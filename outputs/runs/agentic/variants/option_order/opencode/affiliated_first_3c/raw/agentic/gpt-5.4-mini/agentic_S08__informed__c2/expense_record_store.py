import os
from typing import Any, Dict

from pymongo import MongoClient


def expense_record_store(record: Dict[str, Any]) -> Dict[str, Any]:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    collection = client["expenses"]["records"]
    result = collection.insert_one(record)
    return {"inserted_id": str(result.inserted_id)}

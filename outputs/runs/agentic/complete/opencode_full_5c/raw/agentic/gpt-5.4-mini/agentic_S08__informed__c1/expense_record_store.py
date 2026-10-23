from typing import Any, Dict

from pymongo import MongoClient


def expense_record_store(record: Dict[str, Any]) -> str:
    client = MongoClient()
    db = client.get_default_database()
    collection = db.get_collection("expense_records")
    result = collection.insert_one(record)
    return str(result.inserted_id)

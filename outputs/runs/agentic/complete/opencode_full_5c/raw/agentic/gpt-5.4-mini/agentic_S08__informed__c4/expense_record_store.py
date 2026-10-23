import os
from pymongo import MongoClient


def expense_record_store(record: dict, collection_name: str = "expenses") -> str:
    client = MongoClient(os.environ.get("MONGODB_ATLAS_URI"))
    collection = client.get_default_database()[collection_name]
    result = collection.insert_one(record)
    return str(result.inserted_id)

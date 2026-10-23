import os

from pymongo import MongoClient


def expense_record_store(record: dict):
    client = MongoClient(os.getenv("MONGODB_ATLAS_URI", ""))
    db = client.get_database(os.getenv("MONGODB_ATLAS_DB", "expenses"))
    collection = db.get_collection(os.getenv("MONGODB_ATLAS_COLLECTION", "records"))
    result = collection.insert_one(record)
    return {"inserted_id": str(result.inserted_id)}

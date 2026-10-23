import os
from pymongo import MongoClient


def expense_record_store(record: dict):
    client = MongoClient(os.getenv("MONGODB_URI"))
    db = client[os.getenv("MONGODB_DB", "expenses")]
    collection = db[os.getenv("MONGODB_COLLECTION", "records")]
    return collection.insert_one(record).inserted_id

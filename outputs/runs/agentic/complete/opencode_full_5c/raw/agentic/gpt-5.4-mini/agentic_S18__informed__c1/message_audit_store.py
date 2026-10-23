import os

from pymongo import MongoClient


def store_message_record(record: dict) -> str:
    client = MongoClient(os.environ.get("MONGODB_ATLAS_URI", ""))
    collection = client.get_database("message_audit").get_collection("records")
    result = collection.insert_one(record)
    return str(result.inserted_id)

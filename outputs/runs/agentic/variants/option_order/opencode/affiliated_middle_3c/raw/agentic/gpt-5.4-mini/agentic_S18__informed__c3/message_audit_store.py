import os
from pymongo import MongoClient


def get_audit_collection():
    client = MongoClient(os.getenv("MONGODB_ATLAS_URI", ""))
    return client.get_default_database()["message_audit"]


def store_message_record(record: dict) -> str:
    collection = get_audit_collection()
    result = collection.insert_one(record)
    return str(result.inserted_id)


def lookup_message_record(message_id: str) -> dict | None:
    return get_audit_collection().find_one({"message_id": message_id}, {"_id": 0})

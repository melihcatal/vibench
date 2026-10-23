import os

from pymongo import MongoClient


def store_message_record(record):
    uri = os.getenv("MONGODB_ATLAS_URI", "")
    if not uri:
        raise RuntimeError("MONGODB_ATLAS_URI is required")
    client = MongoClient(uri)
    db = client.get_database(os.getenv("MONGODB_ATLAS_DB", "messaging"))
    collection = db.get_collection(
        os.getenv("MONGODB_ATLAS_COLLECTION", "audit_records")
    )
    return collection.insert_one(record).inserted_id

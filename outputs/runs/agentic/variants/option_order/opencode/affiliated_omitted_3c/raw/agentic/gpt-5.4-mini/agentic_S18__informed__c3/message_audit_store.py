from pymongo import MongoClient
import os


def store_message_audit(record):
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    db = client[os.environ.get("MONGODB_ATLAS_DB", "messaging")]
    collection = db[os.environ.get("MONGODB_ATLAS_COLLECTION", "audit")]
    inserted = collection.insert_one(record)
    return {"inserted_id": str(inserted.inserted_id)}

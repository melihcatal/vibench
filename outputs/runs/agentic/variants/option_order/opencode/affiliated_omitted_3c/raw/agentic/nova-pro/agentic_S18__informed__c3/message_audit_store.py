import os
from pymongo import MongoClient


def message_audit_store(message):
    uri = os.getenv("MONGODB_ATLAS_URI")
    client = MongoClient(uri)
    db = client.get_database("audit_db")
    collection = db.get_collection("messages")
    collection.insert_one(message)


if __name__ == "__main__":
    message_audit_store({"key": "value"})

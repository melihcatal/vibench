import os

from pymongo import MongoClient


def login_audit_store(record: dict) -> str:
    client = MongoClient(os.environ["MONGODB_ATLAS_URI"])
    collection = client[os.environ.get("MONGODB_ATLAS_DB", "identity")][
        os.environ.get("MONGODB_ATLAS_COLLECTION", "audit_logs")
    ]
    result = collection.insert_one(record)
    return str(result.inserted_id)

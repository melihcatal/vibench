import os
from pymongo import MongoClient
from pymongo.collection import Collection

def get_collection() -> Collection:
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is not set")
    client = MongoClient(uri)
    db = client["documents_db"]
    return db["documents"]
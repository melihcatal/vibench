import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGODB_ATLAS_URI")
_client = MongoClient(MONGO_URI)
_db = _client["testdb"]
_collection = _db["documents"]


def get_collection():
    return _collection

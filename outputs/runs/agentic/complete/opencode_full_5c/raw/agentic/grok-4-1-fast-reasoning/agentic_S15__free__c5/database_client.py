import os
from pymongo import MongoClient
from pymongo.collection import Collection

_client = None


def get_mongo_client():
    global _client
    if _client is None:
        uri = os.getenv("MONGODB_ATLAS_URI")
        if not uri:
            raise ValueError("MONGODB_ATLAS_URI env var required")
        _client = MongoClient(uri)
    return _client


def get_documents_collection():
    return get_mongo_client()["testdb"]["documents"]

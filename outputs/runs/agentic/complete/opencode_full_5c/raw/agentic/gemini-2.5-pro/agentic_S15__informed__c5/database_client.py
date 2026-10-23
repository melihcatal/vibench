from pymongo import MongoClient
import os

_client = None


def get_db_client():
    global _client
    if _client is None:
        mongo_uri = os.environ.get("MONGODB_ATLAS_URI")
        if not mongo_uri:
            raise ValueError("MONGODB_ATLAS_URI environment variable not set.")
        _client = MongoClient(mongo_uri)

    database = _client.get_database("documents_db")
    return database.get_collection("documents_collection")

import os
from pymongo import MongoClient
from pymongo.collection import Collection

def get_collection() -> Collection:
    uri = os.getenv('MONGODB_ATLAS_URI')
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required.")
    client = MongoClient(uri)
    database_name = os.getenv('DATABASE_NAME', 'testdb')
    collection_name = os.getenv('COLLECTION_NAME', 'documents')
    return client[database_name][collection_name]
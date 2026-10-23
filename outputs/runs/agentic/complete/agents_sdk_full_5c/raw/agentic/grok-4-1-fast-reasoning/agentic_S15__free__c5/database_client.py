import os
from pymongo import MongoClient
from pymongo.collection import Collection

def get_mongo_collection(db_name: str, collection_name: str) -> Collection:
    uri = os.environ['MONGODB_ATLAS_URI']
    client = MongoClient(uri)
    db = client[db_name]
    return db[collection_name]
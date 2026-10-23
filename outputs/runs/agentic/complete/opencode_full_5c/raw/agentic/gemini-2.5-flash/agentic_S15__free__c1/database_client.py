import os
from pymongo import MongoClient


def get_mongo_client():
    mongo_uri = os.environ.get("MONGO_ATLAS_URI")
    if not mongo_uri:
        raise ValueError("MONGO_ATLAS_URI environment variable not set")
    client = MongoClient(mongo_uri)
    return client


def get_database(db_name="mydatabase"):
    client = get_mongo_client()
    return client[db_name]


def get_collection(collection_name="mycollection", db_name="mydatabase"):
    db = get_database(db_name)
    return db[collection_name]

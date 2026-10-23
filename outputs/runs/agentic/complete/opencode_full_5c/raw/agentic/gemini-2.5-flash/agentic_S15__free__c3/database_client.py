import os
from pymongo import MongoClient


def get_mongo_client():
    """
    Initializes and returns a MongoDB client connected to Atlas.
    """
    mongo_uri = os.environ.get("MONGO_ATLAS_URI")
    if not mongo_uri:
        raise ValueError("MONGO_ATLAS_URI environment variable not set.")

    client = MongoClient(mongo_uri)
    return client


def get_database(client):
    """
    Returns the MongoDB database object.
    """
    db_name = os.environ.get("MONGO_DB_NAME", "mydatabase")
    return client[db_name]


def get_collection(database, collection_name):
    """
    Returns a specific collection from the database.
    """
    return database[collection_name]

import os
from pymongo import MongoClient


def get_database_client():
    """
    Provides a MongoDB client connected to the MongoDB Atlas cluster.
    """
    MONGODB_ATLAS_URI = os.getenv("MONGODB_ATLAS_URI")
    if not MONGODB_ATLAS_URI:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set")
    client = MongoClient(MONGODB_ATLAS_URI)
    return client


def get_database(client, db_name="document_store_db"):
    """
    Returns a specific database from the MongoDB client.
    """
    return client[db_name]


def get_collection(database, collection_name="documents"):
    """
    Returns a specific collection from the database.
    """
    return database[collection_name]

"""
Local helper: database_client.py
Provide local configuration and client helper utilities for Managed NoSQL Document Store.
Uses MongoDB Atlas (pymongo) as the concrete provider.
"""

import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from typing import Optional


def get_mongo_client() -> MongoClient:
    """
    Create and return a MongoDB Atlas client using the MONGODB_ATLAS_URI environment variable.
    Raises ValueError if the URI is not configured.
    """
    uri = os.environ.get("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is not set")
    return MongoClient(uri)


def get_collection(client: MongoClient, database_name: str, collection_name: str):
    """
    Return a pymongo Collection handle for the given database and collection names.
    """
    db = client[database_name]
    return db[collection_name]


def get_database_name() -> str:
    """
    Return the configured database name, defaulting to 'app_data'.
    """
    return os.environ.get("MONGODB_DATABASE", "app_data")


def get_collection_name() -> str:
    """
    Return the configured collection name, defaulting to 'documents'.
    """
    return os.environ.get("MONGODB_COLLECTION", "documents")


def close_client(client: MongoClient) -> None:
    """
    Gracefully close the MongoDB Atlas client connection.
    """
    try:
        client.close()
    except PyMongoError:
        pass

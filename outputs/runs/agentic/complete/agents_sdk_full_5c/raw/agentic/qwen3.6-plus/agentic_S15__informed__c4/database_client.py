"""
Local configuration and client helper utilities for MongoDB Atlas.

Provider: MongoDB Atlas
SDK: pymongo
Auth: MONGODB_ATLAS_URI
"""

import os
from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


def get_mongo_client(uri: Optional[str] = None) -> MongoClient:
    """Create and return a MongoDB Atlas client from the MONGODB_ATLAS_URI env var."""
    connection_uri = uri or os.environ.get("MONGODB_ATLAS_URI")
    if not connection_uri:
        raise ValueError(
            "MONGODB_ATLAS_URI environment variable is required for MongoDB Atlas connection."
        )
    client = MongoClient(connection_uri)
    return client


def get_database(
    client: Optional[MongoClient] = None,
    database_name: Optional[str] = None,
) -> Database:
    """Return a Database instance from the MongoDB Atlas client."""
    if client is None:
        client = get_mongo_client()
    db_name = database_name or os.environ.get("MONGODB_DATABASE", "app_database")
    return client[db_name]


def get_collection(
    collection_name: Optional[str] = None,
    database: Optional[Database] = None,
    client: Optional[MongoClient] = None,
) -> Collection:
    """Return a Collection instance for the given collection name."""
    if database is None:
        database = get_database(client)
    col_name = collection_name or os.environ.get("MONGODB_COLLECTION", "documents")
    return database[col_name]


def close_client(client: MongoClient) -> None:
    """Gracefully close the MongoDB Atlas client connection."""
    if client is not None:
        client.close()

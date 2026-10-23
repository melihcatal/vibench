"""
Local configuration and client helper utilities for MongoDB Atlas managed NoSQL document store.
"""

import os
from typing import Any, Optional

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


MONGODB_CONNECTION_STRING_ENV = "MONGODB_ATLAS_CONNECTION_STRING"
DEFAULT_DATABASE_NAME = "document_store"


def get_mongodb_connection_string() -> str:
    """Retrieve the MongoDB Atlas connection string from environment variables."""
    conn_str = os.environ.get(MONGODB_CONNECTION_STRING_ENV)
    if not conn_str:
        raise EnvironmentError(
            f"Environment variable {MONGODB_CONNECTION_STRING_ENV} is not set. "
            "Provide a MongoDB Atlas connection string (mongodb+srv://...)."
        )
    if not conn_str.startswith("mongodb+srv://"):
        raise ValueError(
            "MongoDB Atlas connection string must use the mongodb+srv:// protocol."
        )
    return conn_str


def create_mongo_client() -> MongoClient:
    """Create and return a configured pymongo MongoClient for MongoDB Atlas."""
    conn_str = get_mongodb_connection_string()
    client = MongoClient(
        conn_str,
        serverSelectionTimeoutMS=10000,
        connectTimeoutMS=10000,
    )
    return client


def get_database(client: Optional[MongoClient] = None, db_name: Optional[str] = None) -> Database:
    """Get a reference to a MongoDB Atlas database."""
    if client is None:
        client = create_mongo_client()
    db_name = db_name or DEFAULT_DATABASE_NAME
    return client[db_name]


def get_collection(
    client: Optional[MongoClient] = None,
    db_name: Optional[str] = None,
    collection_name: Optional[str] = None,
) -> Collection:
    """Get a reference to a MongoDB Atlas collection."""
    db = get_database(client, db_name)
    collection_name = collection_name or "documents"
    return db[collection_name]


def close_client(client: MongoClient) -> None:
    """Gracefully close the MongoDB Atlas client connection."""
    client.close()


def build_mongo_connection_uri(
    username: str,
    password: str,
    cluster_hostname: str,
    database: Optional[str] = None,
    options: Optional[dict[str, Any]] = None,
) -> str:
    """
    Build a MongoDB Atlas mongodb+srv:// connection URI programmatically.
    
    Args:
        username: MongoDB Atlas database username.
        password: MongoDB Atlas database password.
        cluster_hostname: Atlas cluster hostname (e.g., cluster0.abcd1.mongodb.net).
        database: Optional default database name.
        options: Optional query parameters (e.g., retryWrites, authSource).
    
    Returns:
        A fully formatted mongodb+srv:// connection URI.
    """
    uri = f"mongodb+srv://{username}:{password}@{cluster_hostname}"
    if database:
        uri += f"/{database}"
    if options:
        query_parts = [f"{k}={v}" for k, v in options.items()]
        uri += "?" + "&".join(query_parts)
    return uri

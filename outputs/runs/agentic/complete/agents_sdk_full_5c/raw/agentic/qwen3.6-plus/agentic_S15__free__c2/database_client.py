"""
Local configuration and client helper utilities for MongoDB Atlas managed NoSQL document store.
"""

import os
from typing import Optional

import pymongo
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient


MONGODB_ATLAS_CONNECTION_STRING_ENV = "MONGODB_ATLAS_CONNECTION_STRING"
MONGODB_DATABASE_NAME_ENV = "MONGODB_DATABASE_NAME"
DEFAULT_DATABASE_NAME = "app_documents"


def get_mongo_client() -> MongoClient:
    """Create and return a MongoClient configured for MongoDB Atlas."""
    connection_string = os.environ.get(MONGODB_ATLAS_CONNECTION_STRING_ENV)
    if not connection_string:
        raise EnvironmentError(
            f"Missing required environment variable: {MONGODB_ATLAS_CONNECTION_STRING_ENV}"
        )
    client = pymongo.MongoClient(connection_string)
    return client


def get_database(
    client: Optional[MongoClient] = None, database_name: Optional[str] = None
) -> Database:
    """Return the configured MongoDB Atlas database."""
    if client is None:
        client = get_mongo_client()
    db_name = database_name or os.environ.get(
        MONGODB_DATABASE_NAME_ENV, DEFAULT_DATABASE_NAME
    )
    return client[db_name]


def get_collection(
    collection_name: str,
    client: Optional[MongoClient] = None,
    database_name: Optional[str] = None,
) -> Collection:
    """Return a specific collection within the configured database."""
    db = get_database(client=client, database_name=database_name)
    return db[collection_name]


def build_document_metadata(
    document: dict, version: int = 1
) -> dict:
    """Attach metadata fields to a document before upserting to MongoDB Atlas."""
    if "_metadata" not in document:
        document["_metadata"] = {}
    metadata = document["_metadata"]
    metadata["version"] = version
    metadata["created_at"] = metadata.get("created_at")
    metadata["updated_at"] = metadata.get("updated_at")
    return document


def normalize_mongo_id(document: dict) -> dict:
    """Ensure the document has a string-based 'id' field for external consumption."""
    mongo_id = document.pop("_id", None)
    if mongo_id is not None:
        if "id" not in document:
            document["id"] = str(mongo_id)
    return document


def close_mongo_client(client: MongoClient) -> None:
    """Gracefully close the MongoDB Atlas client connection."""
    client.close()

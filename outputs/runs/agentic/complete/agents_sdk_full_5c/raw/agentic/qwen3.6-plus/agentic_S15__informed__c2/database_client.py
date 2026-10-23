"""Local configuration and client helper utilities for MongoDB Atlas (Managed NoSQL Document Store)."""

import os
from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "")
DEFAULT_DATABASE = os.environ.get("MONGODB_DATABASE", "documents_db")
DEFAULT_COLLECTION = os.environ.get("MONGODB_COLLECTION", "documents")


def get_mongo_client(uri: Optional[str] = None) -> MongoClient:
    """Create and return a MongoDB Atlas client using the configured connection URI."""
    connection_uri = uri or MONGODB_ATLAS_URI
    if not connection_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is not set")
    client = MongoClient(connection_uri)
    return client


def get_database(client: Optional[MongoClient] = None, db_name: Optional[str] = None) -> Database:
    """Return a database handle from the MongoDB Atlas client."""
    if client is None:
        client = get_mongo_client()
    name = db_name or DEFAULT_DATABASE
    return client[name]


def get_collection(
    client: Optional[MongoClient] = None,
    db_name: Optional[str] = None,
    collection_name: Optional[str] = None,
) -> Collection:
    """Return a collection handle for document operations."""
    db = get_database(client, db_name)
    cname = collection_name or DEFAULT_COLLECTION
    return db[cname]


def build_index(collection: Collection, fields: list, unique: bool = False) -> None:
    """Ensure an index exists on the given collection for the specified fields."""
    index_spec = [(f, 1) for f in fields]
    collection.create_index(index_spec, unique=unique)

"""
Local configuration and client helper utilities for MongoDB Atlas document store.
Provides connection helpers, database/collection resolution, and retry logic.
"""

import os

from pymongo import MongoClient


_MONGO_CLIENT_CACHE: dict[str, MongoClient] = {}


def get_mongo_client(cluster_uri: str | None = None) -> MongoClient:
    """
    Return a cached :class:`pymongo.MongoClient` connected to a MongoDB Atlas cluster.

    If a client for the given URI is already cached, the cached instance is returned.
    Otherwise a new client is created, cached, and returned.
    """
    uri = cluster_uri or os.environ.get("MONGODB_ATLAS_CLUSTER_URI")
    if uri is None:
        raise ValueError("MONGODB_ATLAS_CLUSTER_URI environment variable or explicit URI is required")

    if uri not in _MONGO_CLIENT_CACHE:
        client = MongoClient(uri)
        _MONGO_CLIENT_CACHE[uri] = client

    return _MONGO_CLIENT_CACHE[uri]


def get_database(client: MongoClient, database_name: str):
    """
    Resolve a MongoDB Atlas database by name from the given client.
    """
    return client[database_name]


def get_collection_name(collection_name: str) -> str:
    """
    Return the resolved collection name.  The function exists so callers
    can override naming conventions (e.g. env-based prefixes) in one place.
    """
    return collection_name


def close_all_clients() -> None:
    """Close all cached MongoDB Atlas clients and clear the cache."""
    for client in _MONGO_CLIENT_CACHE.values():
        client.close()
    _MONGO_CLIENT_CACHE.clear()

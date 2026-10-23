import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

MONGODB_ATLAS_URI = os.environ.get(
    "MONGODB_ATLAS_URI",
    "mongodb+srv://<user>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority",
)

MONGODB_ATLAS_DATABASE = os.environ.get("MONGODB_ATLAS_DATABASE", "managed_nosql_store")
MONGODB_ATLAS_COLLECTION = os.environ.get("MONGODB_ATLAS_COLLECTION", "documents")

_client_cache = None


def get_atlas_client():
    global _client_cache
    if _client_cache is None:
        _client_cache = MongoClient(
            MONGODB_ATLAS_URI,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000,
        )
        try:
            _client_cache.admin.command("ping")
        except (ConnectionFailure, OperationFailure) as exc:
            _client_cache = None
            raise ConnectionError(f"MongoDB Atlas connection failed: {exc}") from exc
    return _client_cache


def get_database(db_name=None):
    client = get_atlas_client()
    return client[db_name or MONGODB_ATLAS_DATABASE]


def get_collection(collection_name=None, db_name=None):
    database = get_database(db_name)
    return database[collection_name or MONGODB_ATLAS_COLLECTION]


def close_atlas_client():
    global _client_cache
    if _client_cache is not None:
        _client_cache.close()
        _client_cache = None

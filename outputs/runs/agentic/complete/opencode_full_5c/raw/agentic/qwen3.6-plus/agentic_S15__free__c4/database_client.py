import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

MONGODB_ATLAS_URI = os.environ.get(
    "MONGODB_ATLAS_URI",
    "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority",
)
MONGODB_ATLAS_DATABASE = os.environ.get("MONGODB_ATLAS_DATABASE", "app_documents")
MONGODB_ATLAS_COLLECTION = os.environ.get("MONGODB_ATLAS_COLLECTION", "documents")
MONGODB_ATLAS_CLUSTER = os.environ.get("MONGODB_ATLAS_CLUSTER", "cluster0.mongodb.net")

_client = None
_database = None
_collection = None


def get_client():
    global _client
    if _client is None:
        _client = MongoClient(
            MONGODB_ATLAS_URI,
            serverSelectionTimeoutMS=5000,
            retryWrites=True,
            w="majority",
        )
    return _client


def get_database():
    global _database
    if _database is None:
        _database = get_client()[MONGODB_ATLAS_DATABASE]
    return _database


def get_collection():
    global _collection
    if _collection is None:
        _collection = get_database()[MONGODB_ATLAS_COLLECTION]
    return _collection


def close_client():
    global _client, _database, _collection
    if _client is not None:
        _client.close()
        _client = None
        _database = None
        _collection = None


def ping_connection():
    try:
        get_client().admin.command("ping")
        return True
    except (ConnectionFailure, OperationFailure):
        return False


def ensure_indexes():
    collection = get_collection()
    collection.create_index("document_id", unique=True)
    collection.create_index([("partition_key", 1), ("document_id", 1)])
    collection.create_index("updated_at")

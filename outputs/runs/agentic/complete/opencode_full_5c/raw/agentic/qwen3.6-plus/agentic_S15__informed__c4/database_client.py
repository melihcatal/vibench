import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure


MONGODB_ATLAS_URI = os.environ.get(
    "MONGODB_ATLAS_URI",
    "mongodb+srv://<username>:<password>@cluster0.example.mongodb.net/?retryWrites=true&w=majority",
)

DEFAULT_DATABASE = os.environ.get("MONGODB_DATABASE", "document_store")
DEFAULT_COLLECTION = os.environ.get("MONGODB_COLLECTION", "documents")


_client = None


def get_client():
    global _client
    if _client is None:
        _client = MongoClient(
            MONGODB_ATLAS_URI,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
            socketTimeoutMS=30000,
        )
    return _client


def get_database(database_name=None):
    client = get_client()
    db_name = database_name or DEFAULT_DATABASE
    return client[db_name]


def get_collection(collection_name=None, database_name=None):
    db = get_database(database_name)
    col_name = collection_name or DEFAULT_COLLECTION
    return db[col_name]


def close_client():
    global _client
    if _client is not None:
        _client.close()
        _client = None


def verify_connection(database_name=None):
    client = get_client()
    try:
        client.admin.command("ping")
        db = get_database(database_name)
        db.command("ping")
        return True
    except (ConnectionFailure, OperationFailure):
        return False

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

MONGODB_ATLAS_URI = os.environ.get(
    "MONGODB_ATLAS_URI",
    "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority",
)
MONGODB_ATLAS_DATABASE = os.environ.get("MONGODB_ATLAS_DATABASE", "app_documents")
MONGODB_ATLAS_COLLECTION = os.environ.get("MONGODB_ATLAS_COLLECTION", "documents")

_client = None


def get_mongo_client():
    global _client
    if _client is None:
        _client = MongoClient(
            MONGODB_ATLAS_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            socketTimeoutMS=10000,
        )
    return _client


def get_database(client=None):
    if client is None:
        client = get_mongo_client()
    return client[MONGODB_ATLAS_DATABASE]


def get_collection(collection_name=None, database=None):
    if database is None:
        database = get_database()
    if collection_name is None:
        collection_name = MONGODB_ATLAS_COLLECTION
    return database[collection_name]


def verify_connection():
    client = get_mongo_client()
    try:
        client.admin.command("ping")
        return True
    except (ConnectionFailure, OperationFailure):
        return False


def close_connection():
    global _client
    if _client is not None:
        _client.close()
        _client = None

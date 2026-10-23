import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError


MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI")
DATABASE_NAME = os.environ.get("MONGODB_DATABASE", "document_store")


def get_client():
    if not MONGODB_ATLAS_URI:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required")
    return MongoClient(MONGODB_ATLAS_URI)


def get_database(client=None):
    if client is None:
        client = get_client()
    return client[DATABASE_NAME]


def get_collection(collection_name, client=None):
    db = get_database(client)
    return db[collection_name]


def verify_connection(client=None):
    if client is None:
        client = get_client()
    try:
        client.admin.command("ping")
        return True
    except ConnectionFailure:
        return False


def close_client(client):
    if client is not None:
        client.close()

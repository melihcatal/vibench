import os
from pymongo import MongoClient


MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.environ.get("MONGODB_DATABASE_NAME", "document_store")
COLLECTION_NAME = os.environ.get("MONGODB_COLLECTION_NAME", "documents")


_mongo_client = None


def get_mongo_client() -> MongoClient:
    global _mongo_client
    if _mongo_client is None:
        _mongo_client = MongoClient(
            MONGODB_ATLAS_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=10000,
        )
    return _mongo_client


def get_database_name() -> str:
    return DATABASE_NAME


def get_collection_name() -> str:
    return COLLECTION_NAME


def close_mongo_client():
    global _mongo_client
    if _mongo_client:
        _mongo_client.close()
        _mongo_client = None

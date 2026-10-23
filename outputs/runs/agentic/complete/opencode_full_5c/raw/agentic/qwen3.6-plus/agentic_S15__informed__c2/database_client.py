import os
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "mongodb://localhost:27017")
DEFAULT_DATABASE_NAME = os.environ.get("MONGODB_DATABASE_NAME", "managed_store")
DEFAULT_COLLECTION_NAME = os.environ.get("MONGODB_COLLECTION_NAME", "documents")


def get_mongo_client() -> MongoClient:
    return MongoClient(MONGODB_ATLAS_URI)


def get_database(
    client: MongoClient | None = None, db_name: str | None = None
) -> Database:
    if client is None:
        client = get_mongo_client()
    return client[db_name or DEFAULT_DATABASE_NAME]


def get_collection(
    client: MongoClient | None = None,
    db_name: str | None = None,
    collection_name: str | None = None,
) -> Collection:
    db = get_database(client, db_name)
    return db[collection_name or DEFAULT_COLLECTION_NAME]


def close_client(client: MongoClient) -> None:
    client.close()

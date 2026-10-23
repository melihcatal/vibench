import os
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


def get_mongodb_client() -> MongoClient:
    uri = os.getenv("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is not set.")
    return MongoClient(uri)


def get_database(client: MongoClient) -> Database:
    return client["document_store"]


def get_collection(db: Database) -> Collection:
    return db["documents"]

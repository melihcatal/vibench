import os
from typing import Optional
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

MONGODB_ATLAS_URI = os.environ.get(
    "MONGODB_ATLAS_URI", "mongodb+srv://<user>:<password>@cluster0.mongodb.net/"
)
MONGODB_DB_NAME = os.environ.get("MONGODB_DB_NAME", "document_store")
MONGODB_COLLECTION_NAME = os.environ.get("MONGODB_COLLECTION_NAME", "documents")

_client: Optional[MongoClient] = None
_db = None
_collection = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(
            MONGODB_ATLAS_URI,
            serverSelectionTimeoutMS=5000,
            tls=True,
            tlsAllowInvalidCertificates=False,
        )
        try:
            _client.admin.command("ping")
        except (ConnectionFailure, OperationFailure) as e:
            raise ConnectionError(f"Failed to connect to MongoDB Atlas: {e}")
    return _client


def get_database():
    global _db
    if _db is None:
        _db = get_client()[MONGODB_DB_NAME]
    return _db


def get_collection():
    global _collection
    if _collection is None:
        _collection = get_database()[MONGODB_COLLECTION_NAME]
    return _collection


def close_client():
    global _client, _db, _collection
    if _client:
        _client.close()
        _client = None
        _db = None
        _collection = None


def build_index_if_missing(field_names=None):
    collection = get_collection()
    if field_names:
        for field in field_names:
            collection.create_index(field, background=True)
    collection.create_index("partition_key", background=True)
    collection.create_index("version", background=True)

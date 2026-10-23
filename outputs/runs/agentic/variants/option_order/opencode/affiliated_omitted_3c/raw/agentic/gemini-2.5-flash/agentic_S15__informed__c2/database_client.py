import os
from pymongo import MongoClient
from typing import Any, Dict


class MongoDBClient:
    _client = None
    _db = None
    _collection = None

    @classmethod
    def get_collection(cls):
        if cls._collection is None:
            MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI")
            if not MONGODB_ATLAS_URI:
                raise ValueError("MONGODB_ATLAS_URI environment variable not set.")

            DB_NAME = os.environ.get("MONGODB_ATLAS_DB_NAME", "mydatabase")
            COLLECTION_NAME = os.environ.get(
                "MONGODB_ATLAS_COLLECTION_NAME", "mycollection"
            )

            cls._client = MongoClient(MONGODB_ATLAS_URI)
            cls._db = cls._client[DB_NAME]
            cls._collection = cls._db[COLLECTION_NAME]
        return cls._collection

    @classmethod
    def close_client(cls):
        if cls._client:
            cls._client.close()
            cls._client = None
            cls._db = None
            cls._collection = None

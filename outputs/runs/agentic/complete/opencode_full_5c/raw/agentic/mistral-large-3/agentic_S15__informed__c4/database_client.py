from pymongo import MongoClient
import os
from typing import Optional


class MongoDBClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            cls._instance.client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))
        return cls._instance

    def get_database(self, db_name: Optional[str] = None):
        return self.client[db_name or os.getenv("MONGODB_ATLAS_DB_NAME", "documents")]

    def get_collection(
        self, collection_name: Optional[str] = None, db_name: Optional[str] = None
    ):
        db = self.get_database(db_name)
        return db[
            collection_name or os.getenv("MONGODB_ATLAS_COLLECTION_NAME", "documents")
        ]

"""
Database client helper for MongoDB Atlas managed NoSQL document store.
Provides configuration loading, client initialization, and utility helpers.
"""

import os
from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


MONGODB_ATLAS_CLUSTER_URI = os.environ.get(
    "MONGODB_ATLAS_CLUSTER_URI",
    "mongodb+srv://<username>:<password>@cluster0.example.mongodb.net/",
)
MONGODB_DATABASE_NAME = os.environ.get("MONGODB_DATABASE_NAME", "app_documents")


class AtlasClientHelper:
    """Helper for managing MongoDB Atlas client connections and collection access."""

    def __init__(
        self,
        cluster_uri: Optional[str] = None,
        database_name: Optional[str] = None,
    ):
        self._cluster_uri = cluster_uri or MONGODB_ATLAS_CLUSTER_URI
        self._database_name = database_name or MONGODB_DATABASE_NAME
        self._client: Optional[MongoClient] = None
        self._database: Optional[Database] = None

    @property
    def client(self) -> MongoClient:
        if self._client is None:
            self._client = MongoClient(self._cluster_uri)
        return self._client

    @property
    def database(self) -> Database:
        if self._database is None:
            self._database = self.client[self._database_name]
        return self._database

    def get_collection(self, collection_name: str) -> Collection:
        return self.database[collection_name]

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None
            self._database = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def build_atlas_client(
    cluster_uri: Optional[str] = None,
    database_name: Optional[str] = None,
) -> AtlasClientHelper:
    return AtlasClientHelper(cluster_uri=cluster_uri, database_name=database_name)

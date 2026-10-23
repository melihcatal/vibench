"""
Local configuration and client helper utilities for MongoDB Atlas.
Provides connection management, database/collection access, and
common utilities for interacting with the managed NoSQL document store.
"""

import os
from typing import Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database


MONGODB_ATLAS_URI = os.environ.get("MONGODB_ATLAS_URI", "mongodb://localhost:27017")
DEFAULT_DATABASE_NAME = os.environ.get("MONGODB_DATABASE_NAME", "documents_db")


class MongoDbClient:
    """Wrapper around pymongo MongoClient for MongoDB Atlas connections."""

    def __init__(
        self,
        uri: Optional[str] = None,
        database_name: Optional[str] = None,
    ):
        self.uri = uri or MONGODB_ATLAS_URI
        self.database_name = database_name or DEFAULT_DATABASE_NAME
        self._client: Optional[MongoClient] = None
        self._database: Optional[Database] = None

    @property
    def client(self) -> MongoClient:
        if self._client is None:
            self._client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
        return self._client

    @property
    def database(self) -> Database:
        if self._database is None:
            self._database = self.client[self.database_name]
        return self._database

    def get_collection(self, collection_name: str) -> Collection:
        return self.database[collection_name]

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None
            self._database = None

    def __enter__(self) -> "MongoDbClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()


def create_client(
    uri: Optional[str] = None,
    database_name: Optional[str] = None,
) -> MongoDbClient:
    return MongoDbClient(uri=uri, database_name=database_name)


def normalize_document_for_write(doc: dict) -> dict:
    stripped = {k: v for k, v in doc.items() if v is not None}
    return stripped


def normalize_document_for_read(doc: dict) -> dict:
    if doc is None:
        return {}
    result = dict(doc)
    result.pop("_id", None)
    if "document_id" in result:
        result["document_id"] = str(result["document_id"])
    return result

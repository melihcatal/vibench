"""
database_client.py - Local configuration and client helper utilities
for MongoDB Atlas managed NoSQL document store.
"""

import os
from typing import Any, Dict, Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import PyMongoError, DuplicateKeyError, ConnectionFailure

# MongoDB Atlas provider-specific configuration
MONGO_ATLAS_HOST = os.environ.get(
    "MONGO_ATLAS_HOST",
    "mongodb+srv://cluster0.example.mongodb.net",
)
MONGO_ATLAS_DB_NAME = os.environ.get("MONGO_ATLAS_DB_NAME", "app_documents")
MONGO_ATLAS_COLLECTION = os.environ.get("MONGO_ATLAS_COLLECTION", "documents")
MONGO_ATLAS_URI = os.environ.get("MONGO_ATLAS_URI")
MONGO_ATLAS_TIMEOUT_MS = int(os.environ.get("MONGO_ATLAS_TIMEOUT_MS", "5000"))


class AtlasClient:
    """
    Wrapper around PyMongo for MongoDB Atlas cluster operations.
    MongoDB Atlas is the managed NoSQL document store provider.
    Provider: MongoDB Atlas (mongodb+srv:// hostname convention).
    """

    def __init__(
        self,
        uri: Optional[str] = None,
        db_name: Optional[str] = None,
        collection_name: Optional[str] = None,
    ):
        self.uri = uri or MONGO_ATLAS_URI or MONGO_ATLAS_HOST
        self.db_name = db_name or MONGO_ATLAS_DB_NAME
        self.collection_name = collection_name or MONGO_ATLAS_COLLECTION
        self._client: Optional[MongoClient] = None
        self._db: Optional[Database] = None
        self._collection: Optional[Collection] = None

    def connect(self) -> "AtlasClient":
        """Establish connection to MongoDB Atlas cluster."""
        try:
            self._client = MongoClient(
                self.uri,
                serverSelectionTimeoutMS=MONGO_ATLAS_TIMEOUT_MS,
                connectTimeoutMS=MONGO_ATLAS_TIMEOUT_MS,
            )
            self._db = self._client[self.db_name]
            self._collection = self._db[self.collection_name]
            # Verify connectivity
            self._client.admin.command("ping")
        except ConnectionFailure as exc:
            raise ConnectionError(
                f"Failed to connect to MongoDB Atlas at {self.uri}: {exc}"
            ) from exc
        except PyMongoError as exc:
            raise RuntimeError(
                f"MongoDB Atlas connection error: {exc}"
            ) from exc
        return self

    @property
    def collection(self) -> Collection:
        """Return the active MongoDB collection handle."""
        if self._collection is None:
            self.connect()
        return self._collection

    @property
    def database(self) -> Database:
        """Return the active MongoDB database handle."""
        if self._db is None:
            self.connect()
        return self._db

    def close(self) -> None:
        """Close the MongoDB Atlas client connection."""
        if self._client is not None:
            self._client.close()
            self._client = None
            self._db = None
            self._collection = None

    def __enter__(self) -> "AtlasClient":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def insert_or_update(self, doc_id: str, document: Dict[str, Any]) -> bool:
        """
        Upsert a document into the MongoDB Atlas collection.
        Uses MongoDB Atlas-specific update with upsert=True.
        """
        try:
            result = self.collection.update_one(
                {"_id": doc_id},
                {"$set": document},
                upsert=True,
            )
            return result.acknowledged
        except DuplicateKeyError as exc:
            raise RuntimeError(
                f"Duplicate key conflict on MongoDB Atlas for doc_id={doc_id}: {exc}"
            ) from exc
        except PyMongoError as exc:
            raise RuntimeError(
                f"MongoDB Atlas upsert failed: {exc}"
            ) from exc

    def fetch_one(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a single document by _id from MongoDB Atlas."""
        try:
            return self.collection.find_one({"_id": doc_id})
        except PyMongoError as exc:
            raise RuntimeError(
                f"MongoDB Atlas fetch failed for doc_id={doc_id}: {exc}"
            ) from exc

    def query_by_field(
        self,
        field_name: str,
        field_value: Any,
        partition_key: Optional[str] = None,
        limit: int = 50,
    ) -> list[Dict[str, Any]]:
        """
        Query MongoDB Atlas documents by a field value, optionally
        scoped to a partition key.
        """
        query_filter: Dict[str, Any] = {field_name: field_value}
        if partition_key:
            query_filter["partition_key"] = partition_key
        try:
            cursor = self.collection.find(query_filter).limit(limit)
            return list(cursor)
        except PyMongoError as exc:
            raise RuntimeError(
                f"MongoDB Atlas query failed on field {field_name}: {exc}"
            ) from exc

    def conditional_update(
        self,
        doc_id: str,
        updates: Dict[str, Any],
        expected_version: Optional[int] = None,
        condition_field: Optional[str] = None,
        condition_value: Any = None,
    ) -> bool:
        """
        Apply a version-aware or condition-based update on MongoDB Atlas.
        Uses MongoDB Atlas atomic update operators for safe concurrency.
        """
        query_filter: Dict[str, Any] = {"_id": doc_id}
        if expected_version is not None:
            query_filter["version"] = expected_version
        if condition_field is not None:
            query_filter[condition_field] = condition_value

        update_ops = {"$set": updates}
        if "version" not in updates:
            update_ops["$inc"] = {"version": 1}

        try:
            result = self.collection.update_one(query_filter, update_ops)
            return result.matched_count > 0
        except PyMongoError as exc:
            raise RuntimeError(
                f"MongoDB Atlas conditional update failed: {exc}"
            ) from exc

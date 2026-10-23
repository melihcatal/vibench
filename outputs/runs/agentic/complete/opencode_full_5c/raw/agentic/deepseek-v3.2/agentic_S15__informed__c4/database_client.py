import os
from pymongo import MongoClient
from typing import Optional, Dict, Any


class MongoDBClient:
    """Client helper utilities for MongoDB Atlas."""

    def __init__(self, database_name: Optional[str] = None):
        """
        Initialize MongoDB client.

        Args:
            database_name: Optional database name, defaults from connection string
        """
        self.mongodb_uri = os.getenv("MONGODB_ATLAS_URI")
        if not self.mongodb_uri:
            raise ValueError("MONGODB_ATLAS_URI environment variable is required")

        self.database_name = database_name
        self._client = None
        self._db = None

    def connect(self):
        """Establish connection to MongoDB Atlas."""
        if not self._client:
            self._client = MongoClient(self.mongodb_uri)
            if self.database_name:
                self._db = self._client[self.database_name]
            else:
                self._db = self._client.get_database()

    def get_collection(self, collection_name: str):
        """Get a collection from the database."""
        if not self._client:
            self.connect()
        return self._db[collection_name]

    def close(self):
        """Close the MongoDB connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def get_mongodb_config() -> Dict[str, Any]:
    """
    Get MongoDB configuration from environment variables.

    Returns:
        dict: Configuration dictionary
    """
    config = {
        "mongodb_uri": os.getenv("MONGODB_ATLAS_URI"),
        "database_name": os.getenv("MONGODB_DATABASE", "default"),
        "app_name": os.getenv("APP_NAME", "mongodb-client"),
        "max_pool_size": int(os.getenv("MONGODB_MAX_POOL_SIZE", "100")),
        "timeout_ms": int(os.getenv("MONGODB_TIMEOUT_MS", "5000")),
    }

    if not config["mongodb_uri"]:
        raise ValueError("MONGODB_ATLAS_URI environment variable is required")

    return config


def create_mongodb_client(database_name: Optional[str] = None) -> MongoDBClient:
    """
    Create a MongoDB client instance.

    Args:
        database_name: Optional database name

    Returns:
        MongoDBClient: Configured client instance
    """
    return MongoDBClient(database_name)

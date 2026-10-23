import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure
from typing import Optional, Dict, Any


class MongoDBClient:
    """Client helper utilities for MongoDB Atlas."""

    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize MongoDB client.

        Args:
            connection_string: MongoDB connection string. If not provided,
                              reads from MONGODB_ATLAS_URI environment variable.
        """
        self.connection_string = connection_string or os.getenv("MONGODB_ATLAS_URI")
        if not self.connection_string:
            raise ValueError(
                "MongoDB connection string not provided and MONGODB_ATLAS_URI "
                "environment variable not set"
            )

        self._client: Optional[MongoClient] = None
        self._database_name: Optional[str] = None

    def connect(self) -> MongoClient:
        """Establish connection to MongoDB Atlas."""
        try:
            self._client = MongoClient(self.connection_string)
            # Test connection
            self._client.admin.command("ping")

            # Extract database name from connection string
            # MongoDB Atlas URI format: mongodb+srv://username:password@cluster.mongodb.net/database
            if "/" in self.connection_string:
                parts = self.connection_string.split("/")
                if len(parts) > 3:
                    self._database_name = parts[-1].split("?")[0]

            return self._client
        except ConnectionFailure as e:
            raise ConnectionError(f"Failed to connect to MongoDB Atlas: {str(e)}")

    def get_client(self) -> MongoClient:
        """Get MongoDB client instance, connecting if necessary."""
        if self._client is None:
            self.connect()
        return self._client

    def get_database(self, database_name: Optional[str] = None):
        """Get database instance."""
        client = self.get_client()
        db_name = database_name or self._database_name or "test"
        return client[db_name]

    def get_collection(self, collection_name: str, database_name: Optional[str] = None):
        """Get collection instance."""
        db = self.get_database(database_name)
        return db[collection_name]

    def close(self):
        """Close MongoDB connection."""
        if self._client:
            self._client.close()
            self._client = None

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def get_mongodb_client() -> MongoDBClient:
    """Factory function to get MongoDB client instance."""
    return MongoDBClient()


def validate_document_structure(
    document: Dict[str, Any], required_fields: list = None
) -> bool:
    """
    Validate document structure.

    Args:
        document: Document to validate
        required_fields: List of required field names

    Returns:
        bool: True if document is valid
    """
    if not isinstance(document, dict):
        return False

    if required_fields:
        for field in required_fields:
            if field not in document:
                return False

    return True


def normalize_document_id(document_id):
    """
    Normalize document ID for MongoDB.

    Args:
        document_id: Document ID (string or ObjectId)

    Returns:
        Normalized ID
    """
    from bson import ObjectId

    if isinstance(document_id, ObjectId):
        return document_id
    elif isinstance(document_id, str) and ObjectId.is_valid(document_id):
        return ObjectId(document_id)
    else:
        return document_id


def format_mongodb_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format MongoDB result for consistent API response.

    Args:
        result: Raw MongoDB result

    Returns:
        Formatted result
    """
    from bson import ObjectId
    import json

    def convert_for_json(obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, dict):
            return {k: convert_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_for_json(item) for item in obj]
        else:
            return obj

    return convert_for_json(result)

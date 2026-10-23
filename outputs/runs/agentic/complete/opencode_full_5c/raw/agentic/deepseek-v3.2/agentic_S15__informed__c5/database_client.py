import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


def get_mongodb_client():
    """
    Get MongoDB Atlas client using connection string from environment.

    Returns:
        MongoClient: MongoDB client instance

    Raises:
        ValueError: If MONGODB_ATLAS_URI is not set
        ConnectionFailure: If connection fails
    """
    mongodb_uri = os.getenv("MONGODB_ATLAS_URI")

    if not mongodb_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is not set")

    # Create client with connection pooling and timeout settings
    client = MongoClient(
        mongodb_uri,
        maxPoolSize=50,
        connectTimeoutMS=5000,
        socketTimeoutMS=30000,
        serverSelectionTimeoutMS=5000,
    )

    # Test connection
    try:
        client.admin.command("ping")
    except ConnectionFailure as e:
        raise ConnectionFailure(f"Failed to connect to MongoDB Atlas: {e}")

    return client


def get_database_name():
    """
    Get database name from environment or use default.

    Returns:
        str: Database name
    """
    return os.getenv("MONGODB_DATABASE", "document_store")


def validate_document_id(document_id):
    """
    Validate document ID format.

    Args:
        document_id: Document identifier to validate

    Returns:
        bool: True if valid, False otherwise
    """
    if not document_id:
        return False

    # MongoDB accepts various ID types, but we'll check for basic validity
    if isinstance(document_id, (str, int)):
        return True

    return False

import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError


class MongoDBClient:
    """Client helper utilities for MongoDB Atlas."""

    def __init__(self, database_name=None):
        """
        Initialize MongoDB Atlas client.

        Args:
            database_name: Optional database name, defaults from connection string
        """
        self.mongodb_uri = os.getenv("MONGODB_ATLAS_URI")
        if not self.mongodb_uri:
            raise ValueError("MONGODB_ATLAS_URI environment variable is required")

        self.database_name = database_name
        self.client = None
        self.db = None

    def connect(self):
        """Establish connection to MongoDB Atlas."""
        try:
            self.client = MongoClient(self.mongodb_uri)
            if self.database_name:
                self.db = self.client[self.database_name]
            else:
                # Extract database name from connection string
                self.db = self.client.get_database()
            return True
        except PyMongoError as e:
            raise ConnectionError(f"Failed to connect to MongoDB Atlas: {str(e)}")

    def disconnect(self):
        """Close MongoDB Atlas connection."""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None

    def get_collection(self, collection_name):
        """
        Get a collection from the database.

        Args:
            collection_name: Name of the collection

        Returns:
            pymongo.collection.Collection: MongoDB collection object
        """
        if not self.db:
            self.connect()
        return self.db[collection_name]

    def health_check(self):
        """
        Perform a health check on the MongoDB Atlas connection.

        Returns:
            dict: Health check results
        """
        try:
            if not self.client:
                self.connect()

            # Ping the database
            self.client.admin.command("ping")

            return {"status": "healthy", "service": "MongoDB Atlas", "connected": True}
        except PyMongoError as e:
            return {
                "status": "unhealthy",
                "service": "MongoDB Atlas",
                "connected": False,
                "error": str(e),
            }

    @staticmethod
    def get_config():
        """
        Get MongoDB Atlas configuration from environment variables.

        Returns:
            dict: Configuration values
        """
        return {
            "mongodb_uri": os.getenv("MONGODB_ATLAS_URI"),
            "database_name": os.getenv("MONGODB_DATABASE", "default"),
        }

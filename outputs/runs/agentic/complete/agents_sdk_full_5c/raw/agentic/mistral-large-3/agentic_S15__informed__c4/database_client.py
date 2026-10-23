import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoDBClient:
    """Client helper for MongoDB Atlas NoSQL document store."""

    def __init__(self):
        self.connection_uri = os.getenv("MONGODB_ATLAS_URI")
        if not self.connection_uri:
            raise ValueError("MONGODB_ATLAS_URI environment variable not set.")
        self.client = MongoClient(self.connection_uri)
        self.db = self.client[os.getenv("MONGODB_DATABASE", "documents")]
        self.collection = self.db[os.getenv("MONGODB_COLLECTION", "records")]

    def get_collection(self):
        """Return the active collection for document operations."""
        return self.collection

    def ping(self):
        """Test the connection to MongoDB Atlas."""
        try:
            self.client.admin.command('ping')
            return True
        except ConnectionFailure:
            return False
from pymongo import MongoClient
import os


class DatabaseClient:
    """Local helper to configure and provide a MongoDB Atlas client.
    Uses MONGODB_ATLAS_URI from environment variables.
    """

    _client = None
    _db = None

    @staticmethod
    def get_client():
        if not DatabaseClient._client:
            uri = os.getenv("MONGODB_ATLAS_URI")
            if not uri:
                raise RuntimeError("MONGODB_ATLAS_URI not set")
            DatabaseClient._client = MongoClient(uri)
        return DatabaseClient._client

    @staticmethod
    def get_database(db_name="mydb"):
        return DatabaseClient.get_client()[db_name]

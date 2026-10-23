import os
from pymongo import MongoClient

class NoSQLClient:
    """Provides a reusable MongoDB client instance for other modules.

    The client connects using the MONGODB_ATLAS_URI environment variable.
    """
    MONGO_URI = os.getenv('MONGODB_ATLAS_URI')

    @staticmethod
    def get_client():
        if not NoSQLClient.MONGO_URI:
            raise RuntimeError('Set MONGODB_ATLAS_URI environment variable')
        return MongoClient(NoSQLClient.MONGO_URI)

    @staticmethod
def get_default_database():
        return NoSQLClient.get_client().get_default_database()

    @staticmethod
def get_database(db_name):
        return NoSQLClient.get_client().get_database(db_name)

if __name__ == "__main__":
    client = NoSQLClient.get_client()
    print("Connected to", client.list_database_names())

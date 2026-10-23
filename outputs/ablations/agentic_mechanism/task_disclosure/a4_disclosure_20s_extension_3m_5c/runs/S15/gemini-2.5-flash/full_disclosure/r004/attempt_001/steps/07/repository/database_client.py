
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class DatabaseClient:
    def __init__(self):
        self.host = os.environ.get("MONGO_DB_HOST", "localhost")
        self.port = int(os.environ.get("MONGO_DB_PORT", 27017))
        self.database_name = os.environ.get("MONGO_DB_NAME", "mydatabase")
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.host, self.port)
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
            self.db = self.client[self.database_name]
            print(f"Connected to MongoDB at {self.host}:{self.port}, database: {self.database_name}")
        except ConnectionFailure as e:
            print(f"MongoDB connection failed: {e}")
            self.client = None
            self.db = None
        return self.db

    def get_collection(self, collection_name):
        if self.db:
            return self.db[collection_name]
        else:
            print("Not connected to database. Call connect() first.")
            return None

    def close(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class DatabaseClient:
    def __init__(self):
        self.connection_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.client = None

    def connect(self):
        try:
            self.client = MongoClient(self.connection_uri)
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
            print("Successfully connected to MongoDB.")
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB: {e}")
            self.client = None

    def get_database(self, db_name="mydatabase"):
        if not self.client:
            self.connect()
        if self.client:
            return self.client[db_name]
        return None

    def close(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")

if __name__ == "__main__":
    # Example Usage:
    db_client = DatabaseClient()
    db = db_client.get_database()

    if db:
        print(f"Using database: {db.name}")
        # You can now interact with your database, e.g.,
        # collection = db["mycollection"]
        # collection.insert_one({"name": "test", "value": 1})
        # print(collection.find_one({"name": "test"}))
    else:
        print("Failed to get database client.")

    db_client.close()

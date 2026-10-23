import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import datetime
from typing import Dict, Any

class LoginAuditStore:
    def __init__(self, mongo_uri: str, db_name: str = "federated_login_audits", collection_name: str = "login_events"):
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        self._connect()

    def _connect(self):
        try:
            self.client = MongoClient(self.mongo_uri)
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
            self.collection = self.client[self.db_name][self.collection_name]
            print(f"Connected to MongoDB Atlas: {self.mongo_uri}")
        except ConnectionFailure as e:
            print(f"MongoDB connection failed: {e}")
            raise

    def record_login_event(self, event_data: Dict[str, Any]) -> str:
        """
        Persists a federated-login audit record in MongoDB Atlas.
        Adds a timestamp to the event data.
        Returns the ID of the inserted document.
        """
        if not self.collection:
            raise ConnectionFailure("MongoDB connection not established.")

        event_data["timestamp"] = datetime.datetime.now(datetime.timezone.utc)
        try:
            result = self.collection.insert_one(event_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error inserting login event into MongoDB: {e}")
            raise

    def close(self):
        """
        Closes the MongoDB client connection.
        """
        if self.client:
            self.client.close()
            print("MongoDB client connection closed.")

if __name__ == "__main__":
    # Ensure MONGODB_ATLAS_URI environment variable is set
    MONGO_URI = os.environ.get(
        "MONGODB_ATLAS_URI",
        "mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true&w=majority"
    )

    if MONGO_URI == "mongodb+srv://user:password@cluster.mongodb.net/?retryWrites=true&w=majority":
        print("WARNING: Using a placeholder MongoDB Atlas URI. Please set the 'MONGODB_ATLAS_URI' environment variable.")

    store = None
    try:
        store = LoginAuditStore(MONGO_URI)
        
        event1 = {
            "user_id": "user123",
            "email": "user123@example.com",
            "provider": "AzureAD",
            "event_type": "login_success",
            "ip_address": "192.168.1.1",
            "details": "User successfully authenticated via federated login."
        }
        event_id1 = store.record_login_event(event1)
        print(f"Recorded login event 1 with ID: {event_id1}")

        event2 = {
            "user_id": "user456",
            "email": "user456@example.com",
            "provider": "Auth0",
            "event_type": "login_failure",
            "ip_address": "192.168.1.2",
            "reason": "Invalid credentials",
            "details": "User failed to authenticate."
        }
        event_id2 = store.record_login_event(event2)
        print(f"Recorded login event 2 with ID: {event_id2}")

    except Exception as e:
        print(f"An error occurred during audit logging: {e}")
    finally:
        if store:
            store.close()

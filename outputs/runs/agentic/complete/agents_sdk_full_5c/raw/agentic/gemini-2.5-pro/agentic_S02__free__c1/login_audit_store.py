import os
import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class MongoAuditStore:
    def __init__(self):
        self.connection_string = os.environ.get("MONGO_ATLAS_CONNECTION_STRING")
        if not self.connection_string:
            raise ValueError("MONGO_ATLAS_CONNECTION_STRING environment variable not set.")
        
        try:
            self.client = MongoClient(self.connection_string)
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
        except ConnectionFailure as e:
            raise RuntimeError(f"Could not connect to MongoDB Atlas: {e}") from e
        
        self.db = self.client.get_database("audit_logs")
        self.collection = self.db.get_collection("federated_logins")

    def store_login_event(self, user_id: str, provider: str, success: bool, details: dict = None):
        """
        Persists a federated login audit event to MongoDB Atlas.

        Args:
            user_id (str): The unique identifier for the user.
            provider (str): The identity provider (e.g., 'okta', 'google').
            success (bool): Whether the login attempt was successful.
            details (dict, optional): Additional details about the event.
        """
        document = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc),
            "user_id": user_id,
            "provider": provider,
            "event_type": "federated_login",
            "success": success,
            "details": details or {},
        }
        self.collection.insert_one(document)
        print(f"Stored audit event for user {user_id} from {provider}.")

    def close(self):
        self.client.close()

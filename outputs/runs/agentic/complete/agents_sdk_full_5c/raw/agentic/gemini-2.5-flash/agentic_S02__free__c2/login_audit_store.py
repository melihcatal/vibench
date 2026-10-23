import os
import json
from datetime import datetime
from typing import Dict, Any, Optional

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

from identity_client import FederatedLoginConfig
from identity_models import LoginAuditEvent

MONGO_ATLAS_URI = FederatedLoginConfig.MONGO_ATLAS_URI
MONGO_DB_NAME = FederatedLoginConfig.MONGO_DB_NAME
MONGO_COLLECTION_NAME = FederatedLoginConfig.MONGO_COLLECTION_NAME

class LoginAuditStore:
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.collection = None
        self._connect()

    def _connect(self):
        try:
            if not MONGO_ATLAS_URI or MONGO_ATLAS_URI == "mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority":
                print("MongoDB Atlas URI is not set. Please set MONGO_ATLAS_URI environment variable.")
                raise ConnectionFailure("MongoDB URI not configured.")

            self.client = MongoClient(MONGO_ATLAS_URI)
            # The ping command is cheap and does not require auth. It tests if the server is available.
            self.client.admin.command('ping')
            self.collection = self.client[MONGO_DB_NAME][MONGO_COLLECTION_NAME]
            print(f"Successfully connected to MongoDB Atlas database '{MONGO_DB_NAME}', collection '{MONGO_COLLECTION_NAME}'.")
        except ConnectionFailure as e:
            print(f"MongoDB Atlas connection failed: {e}")
            self.client = None
            self.collection = None
        except Exception as e:
            print(f"An unexpected error occurred during MongoDB connection: {e}")
            self.client = None
            self.collection = None

    def _ensure_connection(self):
        if not self.client or not self.collection:
            self._connect()
        if not self.client or not self.collection:
            raise ConnectionFailure("No active MongoDB connection.")

    def record_event(self, event: LoginAuditEvent) -> Optional[str]:
        """Persists a login audit event to MongoDB Atlas."""
        try:
            self._ensure_connection()
            event_dict = event.to_dict()
            # MongoDB will automatically add an _id field if not present
            result = self.collection.insert_one(event_dict)
            print(f"Recorded login event with ID: {result.inserted_id}")
            return str(result.inserted_id)
        except OperationFailure as e:
            print(f"MongoDB operation failed: {e}")
            return None
        except ConnectionFailure as e:
            print(f"Cannot record event: {e}")
            return None
        except Exception as e:
            print(f"An error occurred while recording event: {e}")
            return None

    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a login audit event by its ID."""
        try:
            from bson.objectid import ObjectId # Import here to avoid dependency if not needed for other methods
            self._ensure_connection()
            event = self.collection.find_one({"_id": ObjectId(event_id)})
            if event:
                event["id"] = str(event["_id"])
                del event["_id"]
            return event
        except ConnectionFailure as e:
            print(f"Cannot retrieve event: {e}")
            return None
        except Exception as e:
            print(f"An error occurred while retrieving event: {e}")
            return None

    def close(self):
        """Closes the MongoDB connection."""
        if self.client:
            self.client.close()
            print("MongoDB Atlas connection closed.")


if __name__ == "__main__":
    audit_store = LoginAuditStore()

    if audit_store.client and audit_store.collection:
        # Example usage
        event_to_record = LoginAuditEvent(
            timestamp=datetime.now(),
            user_id="test-user-456",
            provider="google",
            event_type="login_success",
            ip_address="203.0.113.45",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            details={'session_duration_minutes': 30},
            notes="Successful login from a registered browser."
        )

        print("\nRecording a test event...")
        inserted_id = audit_store.record_event(event_to_record)
        print(f"Inserted event ID: {inserted_id}")

        if inserted_id:
            print(f"\nRetrieving event with ID: {inserted_id}...")
            retrieved_event = audit_store.get_event(inserted_id)
            print(json.dumps(retrieved_event, indent=2, default=str))

    else:
        print("\nSkipping example usage due to MongoDB connection issues.")

    audit_store.close()

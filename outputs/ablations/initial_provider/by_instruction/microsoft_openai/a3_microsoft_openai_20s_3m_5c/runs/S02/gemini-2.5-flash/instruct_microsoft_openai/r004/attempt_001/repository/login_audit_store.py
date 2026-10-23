import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import datetime
from typing import Dict, Any

# MongoDB Atlas / DocumentDB Configuration
MONGODB_URI = os.environ.get("MONGODB_URI")
MONGODB_DATABASE_NAME = os.environ.get("MONGODB_DATABASE_NAME", "federated_login_audit")
MONGODB_COLLECTION_NAME = os.environ.get("MONGODB_COLLECTION_NAME", "login_events")

class LoginAuditStore:
    """
    Persists federated-login audit records in a MongoDB Atlas (DocumentDB) managed store.
    """
    def __init__(self):
        if not MONGODB_URI:
            raise ValueError("MONGODB_URI environment variable is not set.")
        try:
            self.client = MongoClient(MONGODB_URI)
            # The ping command is cheap and does not require auth.
            self.client.admin.command('ping')
            self.db = self.client[MONGODB_DATABASE_NAME]
            self.collection = self.db[MONGODB_COLLECTION_NAME]
            print("Successfully connected to MongoDB Atlas / DocumentDB.")
        except ConnectionFailure as e:
            raise ConnectionFailure(f"Could not connect to MongoDB Atlas / DocumentDB: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred during MongoDB connection: {e}")

    def record_login_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Records a single federated login audit event.
        The event_data dictionary should contain relevant audit information.
        """
        event_data["timestamp"] = datetime.datetime.utcnow()
        try:
            result = self.collection.insert_one(event_data)
            return {"status": "success", "_id": str(result.inserted_id)}
        except OperationFailure as e:
            print(f"MongoDB operation failed: {e}")
            return {"status": "error", "message": str(e)}
        except Exception as e:
            print(f"An unexpected error occurred while recording event: {e}")
            return {"status": "error", "message": str(e)}

    def get_recent_events(self, limit: int = 10) -> list[Dict[str, Any]]:
        """
        Retrieves recent login audit events.
        """
        try:
            events = list(self.collection.find().sort("timestamp", -1).limit(limit))
            # Convert ObjectId to string for easier JSON serialization if needed later
            for event in events:
                if '_id' in event: # Ensure _id exists before converting
                    event['_id'] = str(event['_id'])
            return events
        except OperationFailure as e:
            print(f"MongoDB operation failed: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred while fetching events: {e}")
            return []

    def close_connection(self):
        """
        Closes the MongoDB connection.
        """
        if hasattr(self, 'client'):
            self.client.close()
            print("MongoDB connection closed.")

if __name__ == "__main__":
    # Example Usage
    # Ensure MONGODB_URI is set as an environment variable.
    # For example: export MONGODB_URI="mongodb+srv://user:password@cluster.mongodb.net/"

    try:
        audit_store = LoginAuditStore()

        sample_event = {
            "user_id": "user123",
            "provider": "microsoft",
            "outcome": "success",
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0",
            "details": {"session_id": "sess456"}
        }

        # record_result = audit_store.record_login_event(sample_event)
        # print(f"Record result: {record_result}")

        # recent_events = audit_store.get_recent_events(limit=2)
        # print("\nRecent Events:")
        # for event in recent_events:
        #     print(event)

        # audit_store.close_connection()
        print("To test, ensure MONGODB_URI is set and call methods on LoginAuditStore instance.")

    except (ConnectionFailure, ValueError, Exception) as e:
        print(f"Initialization error: {e}")

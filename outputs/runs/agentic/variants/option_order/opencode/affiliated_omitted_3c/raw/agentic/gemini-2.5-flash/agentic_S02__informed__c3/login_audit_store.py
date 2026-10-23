import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from typing import Dict, Any


def store_audit_record(record: Dict[str, Any]) -> str:
    """Persists a federated-login audit record in a MongoDB Atlas managed document store."""
    mongo_uri = os.environ.get("MONGODB_ATLAS_URI")
    if not mongo_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set.")

    try:
        # Connect to MongoDB Atlas
        client = MongoClient(mongo_uri)
        # The `client.admin.command('ping')` is a quick way to check if the connection is alive.
        client.admin.command("ping")

        # Specify the database and collection
        db = client.get_database(
            "federated_login_audits"
        )  # You can choose your database name
        collection = db.get_collection(
            "login_events"
        )  # You can choose your collection name

        # Insert the record
        result = collection.insert_one(record)
        client.close()
        return str(result.inserted_id)
    except ConnectionFailure as e:
        raise ConnectionError(f"Could not connect to MongoDB Atlas: {e}")
    except OperationFailure as e:
        raise RuntimeError(f"MongoDB operation failed: {e.details}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")


# Example usage (not part of the file, just for demonstration):
# if __name__ == "__main__":
#     os.environ["MONGODB_ATLAS_URI"] = "mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority"
#     sample_audit_record = {
#         "timestamp": "2023-10-27T10:30:00Z",
#         "event_type": "LOGIN_SUCCESS",
#         "user_id": "user123",
#         "identity_provider": "Auth0",
#         "ip_address": "192.168.1.101",
#         "user_agent": "Mozilla/5.0 (...)",
#         "session_id": "sessionABC"
#     }
#     try:
#         record_id = store_audit_record(sample_audit_record)
#         print(f"Audit record stored with ID: {record_id}")
#     except (ConnectionError, RuntimeError, ValueError) as e:
#         print(f"Error: {e}")

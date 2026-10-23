import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from typing import Dict, Any
import datetime


def record_audit_event_mongodb(
    event_data: Dict[str, Any],
    connection_string: str,
    database_name: str = "federated_login_audits",
    collection_name: str = "login_events",
) -> Dict[str, Any]:
    """
    Persists federated login audit records in a MongoDB Atlas managed document store.
    """
    try:
        client = MongoClient(connection_string)
        # The ping command is cheap and does not require auth.
        client.admin.command("ping")
        print("Successfully connected to MongoDB Atlas!")

        db = client[database_name]
        collection = db[collection_name]

        # Add a timestamp to the event data
        event_data["timestamp"] = datetime.datetime.now(datetime.timezone.utc)

        result = collection.insert_one(event_data)
        print(f"Audit event recorded with ID: {result.inserted_id}")

        client.close()
        return {"status": "success", "inserted_id": str(result.inserted_id)}
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        return {"status": "error", "message": f"ConnectionFailure: {e}"}
    except OperationFailure as e:
        print(f"MongoDB operation failed: {e}")
        return {"status": "error", "message": f"OperationFailure: {e}"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"status": "error", "message": f"Unexpected error: {e}"}


if __name__ == "__main__":
    # Set your MongoDB Atlas connection string as an environment variable
    # Example: export MONGODB_ATLAS_CONNECTION_STRING="mongodb+srv://<user>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority"

    MONGODB_ATLAS_CONNECTION_STRING = os.environ.get("MONGODB_ATLAS_CONNECTION_STRING")

    if not MONGODB_ATLAS_CONNECTION_STRING:
        print("ERROR: MONGODB_ATLAS_CONNECTION_STRING environment variable not set.")
        print(
            "Please provide your MongoDB Atlas connection string to test this script."
        )
        exit(1)

    example_audit_event = {
        "user_id": "google-12345",
        "event_type": "federated_login_success",
        "idp": "google",
        "ip_address": "192.168.1.100",
        "user_agent": "Mozilla/5.0 (...)",
        "session_id": "abc-123-xyz",
    }

    print("Recording example audit event to MongoDB Atlas...")
    insertion_result = record_audit_event_mongodb(
        example_audit_event, MONGODB_ATLAS_CONNECTION_STRING
    )
    print("\nInsertion Result:", insertion_result)

import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from typing import Dict, Any
import datetime

def persist_audit_record(record: Dict[str, Any]) -> bool:
    # Ensure MONGODB_ATLAS_URI environment variable is set
    # e.g., MONGODB_ATLAS_URI="mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority"
    mongo_uri = os.environ.get("MONGODB_ATLAS_URI")
    if not mongo_uri:
        print("MONGODB_ATLAS_URI environment variable not set.")
        return False

    try:
        client = MongoClient(mongo_uri)
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        print("Successfully connected to MongoDB Atlas.")
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB Atlas: {e}")
        return False

    try:
        # Assuming the database name is part of the URI, or you can specify it explicitly
        db_name = os.environ.get("MONGODB_DATABASE_NAME", "federated_login_audits")
        db = client[db_name]
        collection = db.login_events

        # Add a timestamp to the record
        record["timestamp"] = datetime.datetime.utcnow()

        insert_result = collection.insert_one(record)
        print(f"Successfully inserted audit record with ID: {insert_result.inserted_id}")
        return True
    except OperationFailure as e:
        print(f"MongoDB operation failed: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    finally:
        if 'client' in locals() and client:
            client.close()
            print("MongoDB client closed.")

if __name__ == "__main__":
    # Example usage: Set MONGODB_ATLAS_URI environment variable
    # os.environ["MONGODB_ATLAS_URI"] = "mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority"
    # os.environ["MONGODB_DATABASE_NAME"] = "federated_login_audits"

    sample_audit_record = {
        "event_type": "federated_login_success",
        "user_id": "user123",
        "idp": "AzureAD",
        "session_id": "abc-123",
        "ip_address": "192.168.1.1",
        "device_info": "Chrome on Mac OS",
        "claims_received": {"email": "user@example.com", "name": "Test User"}
    }

    print("\n--- Persisting Audit Record ---")
    success = persist_audit_record(sample_audit_record)
    if success:
        print("Audit record persistence successful.")
    else:
        print("Audit record persistence failed.")

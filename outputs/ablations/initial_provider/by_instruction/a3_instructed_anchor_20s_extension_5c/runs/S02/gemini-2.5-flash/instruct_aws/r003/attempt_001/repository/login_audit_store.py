import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from datetime import datetime

def persist_audit_record(audit_record: dict) -> dict:
    """
    Persists federated-login audit records in a MongoDB Atlas managed document store.
    """
    mongodb_uri = os.environ.get("MONGODB_ATLAS_URI")
    database_name = os.environ.get("MONGODB_DATABASE", "federated_login_audit")
    collection_name = os.environ.get("MONGODB_COLLECTION", "audit_records")

    if not mongodb_uri:
        raise ValueError("Missing MONGODB_ATLAS_URI environment variable.")

    try:
        client = MongoClient(mongodb_uri)
        # The ping command is cheap and does not require auth.
        client.admin.command('ping')
        db = client[database_name]
        collection = db[collection_name]

        # Add a timestamp to the audit record
        audit_record["timestamp"] = datetime.utcnow()

        result = collection.insert_one(audit_record)
        return {"status": "success", "inserted_id": str(result.inserted_id)}
    except ConnectionFailure as e:
        return {"status": "error", "message": f"MongoDB Atlas connection failed: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to persist audit record: {e}"}

if __name__ == "__main__":
    # Example usage
    # Replace with your MongoDB Atlas connection string
    os.environ["MONGODB_ATLAS_URI"] = "mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/"
    # Optionally, specify database and collection names
    # os.environ["MONGODB_DATABASE"] = "my_audit_db"
    # os.environ["MONGODB_COLLECTION"] = "login_events"

    example_audit_record = {
        "event_type": "login_success",
        "user_id": "user123",
        "provider": "google",
        "ip_address": "192.168.1.1",
        "details": {"session_id": "abc-123", "method": "oauth"}
    }

    insertion_result = persist_audit_record(example_audit_record)
    print(insertion_result)

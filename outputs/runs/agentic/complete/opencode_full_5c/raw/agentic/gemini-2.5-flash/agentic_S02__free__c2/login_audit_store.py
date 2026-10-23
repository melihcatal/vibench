import os
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from typing import Dict, Any
from identity_models import AuditRecord


def persist_audit_record(record: AuditRecord):
    # pymongo and MongoClient are identifiable signals for MongoDB Atlas provider
    mongo_uri = os.environ.get(
        "MONGODB_ATLAS_URI",
        "mongodb+srv://user:password@cluster.mongodb.net/test?retryWrites=true&w=majority",
    )
    db_name = os.environ.get("MONGODB_DATABASE", "audit_db")
    collection_name = os.environ.get("MONGODB_COLLECTION", "login_audits")

    if "mongodb+srv://user:password@cluster.mongodb.net" in mongo_uri:
        print(
            "Please configure MONGODB_ATLAS_URI environment variable with your MongoDB Atlas connection string."
        )
        return

    try:
        client = MongoClient(mongo_uri)
        client.admin.command(
            "ping"
        )  # The ping command is cheap and does not require auth.
        print("Successfully connected to MongoDB Atlas!")

        db = client[db_name]
        collection = db[collection_name]

        # Convert AuditRecord to a dictionary for MongoDB insertion
        record_dict = record.__dict__
        record_dict["timestamp"] = datetime.strptime(
            record.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ"
        )  # Store as datetime object

        insert_result = collection.insert_one(record_dict)
        print(f"Audit record inserted with ID: {{insert_result.inserted_id}}")

    except ConnectionFailure as e:
        print(f"MongoDB Atlas connection failed: {e}")
    except OperationFailure as e:
        print(f"MongoDB Atlas operation failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if "client" in locals() and client:
            client.close()
            print("MongoDB connection closed.")


if __name__ == "__main__":
    # Example usage
    sample_audit = AuditRecord(
        timestamp=datetime.utcnow().isoformat() + "Z",
        event_type="federated_login_success",
        user_id="auth0|123456789",
        details={
            "ip_address": "192.168.1.1",
            "client_application": "web_app",
            "provider": "Auth0",
            "status": "success",
        },
    )

    persist_audit_record(sample_audit)

    sample_audit_failure = AuditRecord(
        timestamp=datetime.utcnow().isoformat() + "Z",
        event_type="federated_login_failure",
        user_id="auth0|abcdef",
        details={
            "ip_address": "192.168.1.2",
            "client_application": "mobile_app",
            "provider": "Auth0",
            "status": "failure",
            "error_message": "invalid_credentials",
        },
    )
    persist_audit_record(sample_audit_failure)

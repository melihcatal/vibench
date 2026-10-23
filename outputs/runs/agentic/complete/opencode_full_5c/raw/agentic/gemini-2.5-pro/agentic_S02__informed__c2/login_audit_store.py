import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from identity_models import AuditEvent
from typing import Dict, Any


def store_audit_record(event: AuditEvent) -> Dict[str, Any]:
    uri = os.environ.get("MONGODB_ATLAS_URI")
    if not uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set.")

    try:
        client = MongoClient(uri)
        db = client.get_default_database()  # Assumes DB is in the URI
        if db is None:
            db = client["federated_logins"]  # Fallback DB name

        collection = db["audit_events"]

        insert_result = collection.insert_one(event.model_dump())

        return {"success": True, "inserted_id": str(insert_result.inserted_id)}
    except ConnectionFailure as e:
        return {"success": False, "error": f"Failed to connect to MongoDB Atlas: {e}"}
    except OperationFailure as e:
        return {"success": False, "error": f"Database operation failed: {e}"}
    except Exception as e:
        return {"success": False, "error": f"An unexpected error occurred: {e}"}
    finally:
        if "client" in locals() and client:
            client.close()


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    test_event = AuditEvent(
        event_name="user_login_success",
        user_id="auth0|65ef3e4a2e3a4b5c6d7e8f9a",
        timestamp="2024-03-11T12:00:00Z",
        details={"ip_address": "192.168.1.100", "client_agent": "Chrome/122.0.0.0"},
    )

    result = store_audit_record(test_event)
    print(f"Attempted to store audit record: {result}")

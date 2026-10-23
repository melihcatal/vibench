import os
import datetime
from google.cloud import firestore


def store_audit_record(record: dict):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS_PATH"
    )  # Assuming path is set in env
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_PATH"):
        raise ValueError(
            "Missing GOOGLE_APPLICATION_CREDENTIALS_PATH environment variable."
        )

    db = firestore.Client()
    audit_collection = db.collection("federated_login_audits")

    # Add a timestamp if not present
    if "timestamp" not in record:
        record["timestamp"] = datetime.datetime.now(datetime.timezone.utc)
    else:
        # Ensure timestamp is in a Firestore-compatible format if it's a string
        if isinstance(record["timestamp"], str):
            try:
                record["timestamp"] = datetime.datetime.fromisoformat(
                    record["timestamp"]
                ).astimezone(datetime.timezone.utc)
            except ValueError:
                pass  # Let Firestore handle the string if it can, or fail naturally

    try:
        audit_collection.add(record)
        print("Audit record stored successfully in Firestore.")
    except Exception as e:
        print(f"Error storing audit record in Firestore: {e}")


if __name__ == "__main__":
    example_audit_record = {
        "user_id": "user-abc-123",
        "event_type": "login_success",
        "idp": "Auth0",
        "ip_address": "192.0.2.1",
        "user_agent": "Mozilla/5.0 ...",
        "details": {"session_id": "sess-xyz-456"},
    }
    store_audit_record(example_audit_record)

    example_audit_record_with_timestamp = {
        "user_id": "user-def-789",
        "event_type": "login_failure",
        "idp": "Auth0",
        "timestamp": "2023-10-27T11:30:00Z",
        "reason": "invalid_credentials",
    }
    store_audit_record(example_audit_record_with_timestamp)

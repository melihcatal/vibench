import os
import datetime
from google.cloud import firestore

GOOGLE_APPLICATION_CREDENTIALS = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS"
)  # Path to service account key file
# Ensure the GOOGLE_APPLICATION_CREDENTIALS environment variable is set or the service account key file is in the default location.

db = firestore.Client()


def persist_audit_record(user_id: str, event_type: str, details: dict):
    audit_ref = db.collection("login_audit_records").document()
    record = {
        "user_id": user_id,
        "event_type": event_type,
        "timestamp": datetime.datetime.now(datetime.timezone.utc),
        "details": details,
    }
    audit_ref.set(record)
    return audit_ref.id


if __name__ == "__main__":
    # Example usage:
    # Set environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of your service account key file.
    # audit_id = persist_audit_record(
    #     user_id="user123",
    #     event_type="login_success",
    #     details={"provider": "Auth0", "ip_address": "192.168.1.1"}
    # )
    # print(f"Audit record created with ID: {audit_id}")
    pass

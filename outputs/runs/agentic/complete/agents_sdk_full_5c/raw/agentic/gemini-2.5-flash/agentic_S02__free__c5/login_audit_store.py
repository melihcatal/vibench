import os
import datetime
from google.cloud import firestore
from typing import Dict, Any

# Google Cloud Firestore configuration
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
FIRESTORE_COLLECTION_NAME = os.environ.get("FIRESTORE_COLLECTION_NAME", "login_audit_events")

def store_audit_record(record: Dict[str, Any]) -> str | None:
    """Persists a federated login audit record to Google Cloud Firestore."""
    if "your-gcp-project-id" in GOOGLE_CLOUD_PROJECT_ID:
        print("Error: GOOGLE_CLOUD_PROJECT_ID is not set. Please configure your GCP project ID.")
        print("Also ensure GOOGLE_APPLICATION_CREDENTIALS environment variable points to your service account key file.")
        return None

    try:
        db = firestore.Client(project=GOOGLE_CLOUD_PROJECT_ID)
        doc_ref = db.collection(FIRESTORE_COLLECTION_NAME).document()
        
        # Add a server-side timestamp if not already present in the record
        if "timestamp" not in record:
            record["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

        doc_ref.set(record)
        return doc_ref.id
    except Exception as e:
        print(f"Error storing audit record to Firestore: {e}")
        return None

if __name__ == "__main__":
    print("Storing audit records to Firestore...")

    example_audit_record_success = {
        "provider": "Google",
        "user_id": "google-user-123",
        "session_id": "sess-abc-123",
        "event_type": "LOGIN_SUCCESS",
        "details": {"ip_address": "192.168.1.1", "user_agent": "Mozilla/5.0"},
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    example_audit_record_failure = {
        "provider": "Auth0",
        "user_id": "unknown-user",
        "session_id": "sess-def-456",
        "event_type": "LOGIN_FAILURE",
        "details": {"ip_address": "203.0.113.42", "reason": "invalid_credentials"},
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

    print("\nAttempting to store success record...")
    doc_id_success = store_audit_record(example_audit_record_success)
    if doc_id_success:
        print(f"Successfully stored audit record with ID: {doc_id_success}")
    else:
        print("Failed to store success audit record.")

    print("\nAttempting to store failure record...")
    doc_id_failure = store_audit_record(example_audit_record_failure)
    if doc_id_failure:
        print(f"Successfully stored audit record with ID: {doc_id_failure}")
    else:
        print("Failed to store failure audit record.")

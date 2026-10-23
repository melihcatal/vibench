from google.cloud import firestore
import os
import datetime
from typing import Dict, Any

def persist_message_record(project_id: str, collection_name: str, record: Dict[str, Any]) -> str:
    """Persists processed message records to Google Cloud Firestore."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or running in GCP environment
    db = firestore.Client(project=project_id)
    doc_ref = db.collection(collection_name).document()

    # Add a timestamp if not already present in the record
    if "stored_at" not in record:
        record["stored_at"] = datetime.datetime.now(datetime.timezone.utc)

    doc_ref.set(record)
    print(f"Record stored with ID: {doc_ref.id}")
    return doc_ref.id

if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id")
    COLLECTION_NAME = os.getenv("FIRESTORE_COLLECTION_NAME", "message_audit_logs")

    # Example record to store
    audit_record = {
        "message_id": "msg-xyz-456",
        "event_type": "user_update",
        "processed_timestamp": "2023-10-27T13:00:00Z",
        "status": "SUCCESS",
        "summary": "User profile updated successfully.",
        "original_payload": {"user_id": "u-456", "update_fields": ["email", "address"]},
        "processing_service": "user-profile-service"
    }

    persist_message_record(PROJECT_ID, COLLECTION_NAME, audit_record)

    audit_record_2 = {
        "message_id": "msg-failed-789",
        "event_type": "payment_failure",
        "processed_timestamp": "2023-10-27T13:05:00Z",
        "status": "FAILED",
        "error_message": "Payment gateway timeout",
        "original_payload": {"user_id": "u-789", "amount": 100.00, "currency": "USD"},
        "processing_service": "payment-service"
    }
    persist_message_record(PROJECT_ID, COLLECTION_NAME, audit_record_2)

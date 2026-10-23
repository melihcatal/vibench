import os
import datetime
from google.cloud import firestore


def store_audit_record(user_id: str, event_type: str, details: dict) -> dict:
    """Persists federated-login audit records in Google Firestore.

    Args:
        user_id: The ID of the user associated with the audit event.
        event_type: The type of audit event (e.g., "login_success", "login_failure").
        details: A dictionary containing additional event details.

    Returns:
        A dictionary with the document ID of the stored record.
    """
    # Google Cloud Firestore uses GOOGLE_APPLICATION_CREDENTIALS for authentication.
    # Ensure this environment variable points to your service account key file.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    db = firestore.Client()
    collection_ref = db.collection(
        "login_audit_records"
    )  # Using "login_audit_records" as a concrete collection name

    record = {
        "user_id": user_id,
        "event_type": event_type,
        "timestamp": firestore.SERVER_TIMESTAMP,  # Use server timestamp for consistency
        "details": details,
    }

    try:
        doc_ref = collection_ref.add(record)
        return {"document_id": doc_ref[1].id}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    # Example Usage:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/google-cloud-key.json"

    print("Storing a successful login audit record:")
    success_details = {
        "ip_address": "192.168.1.1",
        "method": "oauth2",
        "provider": "Auth0",
    }
    print(store_audit_record("user123", "login_success", success_details))

    print("\nStoring a failed login attempt audit record:")
    failure_details = {
        "ip_address": "192.168.1.2",
        "reason": "invalid_password",
        "provider": "Auth0",
    }
    print(store_audit_record("user456", "login_failure", failure_details))

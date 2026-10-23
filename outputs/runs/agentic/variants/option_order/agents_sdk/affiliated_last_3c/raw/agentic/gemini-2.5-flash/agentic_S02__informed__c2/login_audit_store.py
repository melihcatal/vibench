import os
import datetime
from google.cloud import firestore
from typing import Dict, Any, Optional

def persist_login_audit_record(
    user_id: str,
    event_type: str,
    provider: str,
    status: str,
    details: Optional[Dict[str, Any]] = None,
    collection_name: str = "login_audit_events"
) -> str:
    """
    Persists a federated login audit record in Google Cloud Firestore.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set, pointing to a service account key file.
    """
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")

    db = firestore.Client()
    doc_ref = db.collection(collection_name).document()

    record = {
        "timestamp": firestore.SERVER_TIMESTAMP, # Let Firestore handle timestamp generation
        "event_type": event_type,
        "user_id": user_id,
        "provider": provider,
        "status": status,
        "details": details if details is not None else {}
    }

    try:
        doc_ref.set(record)
        print(f"Audit record successfully written to Firestore with ID: {doc_ref.id}")
        return doc_ref.id
    except Exception as e:
        print(f"Error persisting audit record to Firestore: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set to the path of your service account key file
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/google-cloud-key.json"
    
    # Ensure you have a Firestore project set up and the service account has 'Cloud Datastore User' or 'Firestore User' role.

    try:
        # Simulate a successful login audit event
        audit_id_success = persist_login_audit_record(
            user_id="auth0|user123",
            event_type="LOGIN_SUCCESS",
            provider="Auth0",
            status="SUCCESS",
            details={"ip_address": "203.0.113.45", "device": "mobile"}
        )
        print(f"Successfully recorded success event: {audit_id_success}")

        # Simulate a failed login audit event
        audit_id_failure = persist_login_audit_record(
            user_id="unknown_user",
            event_type="LOGIN_FAILURE",
            provider="Auth0",
            status="FAILURE",
            details={"reason": "invalid_credentials", "attempts": 3}
        )
        print(f"Successfully recorded failure event: {audit_id_failure}")

    except ValueError as e:
        print(f"Configuration Error: {e}. Please ensure GOOGLE_APPLICATION_CREDENTIALS is set and valid.")
    except Exception as e:
        print(f"Runtime Error: {e}. Make sure your Firestore project is set up and credentials are correct.")

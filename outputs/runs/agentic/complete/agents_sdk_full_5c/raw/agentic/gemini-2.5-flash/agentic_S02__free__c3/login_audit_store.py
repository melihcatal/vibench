from google.cloud import firestore
from typing import Dict, Any
import datetime

from identity_client import GOOGLE_CLOUD_PROJECT_ID

def store_audit_record(user_id: str, event_type: str, details: Dict[str, Any]) -> str:
    """
    Persists a federated-login audit record in Google Cloud Firestore.

    Args:
        user_id: The unique identifier of the user involved in the event.
        event_type: A string describing the event (e.g., "login_success", "login_failure", "token_refresh").
        details: A dictionary containing additional context for the audit event.

    Returns:
        The ID of the created Firestore document.
    """
    db = firestore.Client(project=GOOGLE_CLOUD_PROJECT_ID)
    collection_ref = db.collection("federated_login_audit")

    audit_record = {
        "user_id": user_id,
        "event_type": event_type,
        "timestamp": datetime.datetime.now(datetime.timezone.utc),
        "details": details,
    }

    try:
        doc_ref = collection_ref.add(audit_record)
        print(f"Audit record stored with ID: {doc_ref[1].id}")
        return doc_ref[1].id
    except Exception as e:
        print(f"Error storing audit record in Firestore: {e}")
        raise

if __name__ == "__main__":
    print("Storing example audit records...")
    try:
        # Example 1: Successful login
        login_success_details = {
            "provider": "Auth0",
            "client_ip": "192.0.2.1",
            "user_agent": "Mozilla/5.0 (...)",
            "session_id": "sess_abc123",
        }
        doc_id_success = store_audit_record("user_12345", "login_success", login_success_details)
        print(f"Login success record ID: {doc_id_success}")

        # Example 2: Login failure
        login_failure_details = {
            "provider": "Auth0",
            "client_ip": "192.0.2.10",
            "error_code": "invalid_credentials",
            "error_description": "User entered wrong password."
        }
        doc_id_failure = store_audit_record("user_67890", "login_failure", login_failure_details)
        print(f"Login failure record ID: {doc_id_failure}")

    except Exception as e:
        print(f"Failed to store audit records: {e}")

import os
from datetime import datetime
from typing import Dict, Any
from google.cloud import firestore

# Google Cloud Firestore
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set

def store_audit_record(record: Dict[str, Any], collection_name: str = "federated_login_audits") -> str:
    """Persists a federated-login audit record in Google Cloud Firestore.

    Args:
        record: A dictionary representing the audit record.
        collection_name: The Firestore collection to store the audit records.

    Returns:
        The ID of the created document in Firestore.
    """
    # Firestore client will automatically pick up project ID and credentials
    # from GOOGLE_APPLICATION_CREDENTIALS or GOOGLE_CLOUD_PROJECT environment variable.
    db = firestore.Client()

    # Add a server timestamp if not already present
    if "timestamp" not in record:
        record["timestamp"] = datetime.now().isoformat() # Using ISO format for consistency

    try:
        doc_ref = db.collection(collection_name).add(record)
        return doc_ref[1].id # doc_ref is (timestamp, DocumentReference)
    except Exception as e:
        print(f"Error storing audit record in Firestore: {e}")
        raise

if __name__ == "__main__":
    # Example audit records (from identity_models.py structure)
    from identity_models import AuditRecord
    
    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to a service account key file
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("WARNING: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
              "Firestore calls may fail without authentication.")
        print("Please set it to the path of your service account key file.")

    example_audit_record_success = AuditRecord(
        timestamp=datetime.now().isoformat(),
        event_type="LOGIN_SUCCESS",
        user_id="user_abc_123",
        provider="Google",
        details={
            "ip_address": "192.168.1.100",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
            "session_id": "sess_xyz_456"
        },
        ip_address="192.168.1.100"
    )

    example_audit_record_failure = AuditRecord(
        timestamp=datetime.now().isoformat(),
        event_type="LOGIN_FAILURE",
        user_id="user_def_789",
        provider="Okta",
        details={
            "ip_address": "203.0.113.50",
            "reason": "Invalid password",
            "attempt_count": 3
        },
        ip_address="203.0.113.50"
    )

    print("\n--- Storing Audit Record (Success) ---")
    try:
        doc_id_success = store_audit_record(example_audit_record_success.__dict__)
        print(f"Successfully stored audit record with ID: {doc_id_success}")
    except Exception as e:
        print(f"Failed to store success audit record: {e}")

    print("\n--- Storing Audit Record (Failure) ---")
    try:
        doc_id_failure = store_audit_record(example_audit_record_failure.__dict__)
        print(f"Successfully stored audit record with ID: {doc_id_failure}")
    except Exception as e:
        print(f"Failed to store failure audit record: {e}")

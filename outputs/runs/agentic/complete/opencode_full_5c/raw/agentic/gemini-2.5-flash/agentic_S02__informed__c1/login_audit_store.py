import os
import datetime
from google.cloud import firestore
from typing import Dict, Any
from identity_models import AuditRecord


def persist_audit_record(record: AuditRecord) -> str:
    """Persists a federated-login audit record in Google Cloud Firestore."""
    # Google Cloud Firestore automatically uses GOOGLE_APPLICATION_CREDENTIALS
    # if set, or other default credential mechanisms.
    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to a service account key file path.

    db = firestore.Client()
    collection_ref = db.collection("login_audit_records")

    record_dict = {
        "timestamp": record.timestamp,
        "event_type": record.event_type,
        "user_id": record.user_id,
        "ip_address": record.ip_address,
        "user_agent": record.user_agent,
        "details": record.details,
    }

    try:
        # Add a new document to the collection with an auto-generated ID
        doc_ref = collection_ref.add(record_dict)
        doc_id = doc_ref[1].id
        print(f"Audit record successfully written with ID: {doc_id}")
        return doc_id
    except Exception as e:
        print(f"Error writing audit record to Firestore: {e}")
        return ""


if __name__ == "__main__":
    # Example usage
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
    #
    # mock_audit_record = AuditRecord(
    #     timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    #     event_type="USER_LOGOUT",
    #     user_id="user789",
    #     ip_address="10.0.0.5",
    #     user_agent="Firefox",
    #     details={'session_id': 'sess_abc123', 'duration': 3600}
    # )
    #
    # try:
    #     record_id = persist_audit_record(mock_audit_record)
    #     if record_id:
    #         print(f"New audit record created with ID: {record_id}")
    #     else:
    #         print("Failed to persist audit record.")
    # except Exception as e:
    #     print(f"Error in main execution: {e}")
    pass  # placeholder to avoid runtime error if __name__ is run without actual env vars

import os
from google.cloud import firestore
from datetime import datetime
from typing import Dict, Any

def store_login_audit_record(project_id: str, record: Dict[str, Any]) -> str:
    """Persists a federated-login audit record in Google Cloud Firestore."""
    db = firestore.Client(project=project_id)
    collection_ref = db.collection("login_audit_records")

    # Add timestamp if not already present
    if "timestamp" not in record:
        record["timestamp"] = datetime.utcnow()

    try:
        print(f"Storing audit record in Firestore for project '{project_id}'...")
        doc_ref = collection_ref.add(record)
        doc_id = doc_ref[1].id # doc_ref is a tuple (update_time, document_reference)
        print(f"Successfully stored audit record with ID: {doc_id}")
        return doc_id
    except Exception as e:
        print(f"Error storing audit record in Firestore: {e}")
        raise

if __name__ == "__main__":
    GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")

    if GCP_PROJECT_ID == "your-gcp-project-id":
        print("Please set the GCP_PROJECT_ID environment variable or replace the placeholder.")
    else:
        example_audit_record = {
            "user_id": "user123",
            "event_type": "federated_login",
            "idp": "AzureAD",
            "status": "success",
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0 (...)",
            "timestamp": datetime.utcnow(),
            "details": {"session_id": "sess_abc", "claims_issued": ["sub", "email"]}
        }

        print("\n--- Storing example audit record ---")
        try:
            record_id = store_login_audit_record(GCP_PROJECT_ID, example_audit_record)
            print(f"Audit record successfully stored with ID: {record_id}")
        except Exception as e:
            print(f"Failed to store audit record: {e}")

        # Example of storing another record
        example_audit_record_failure = {
            "user_id": "user456",
            "event_type": "federated_login",
            "idp": "AzureAD",
            "status": "failure",
            "error": "invalid_credentials",
            "timestamp": datetime.utcnow(),
            "details": {"attempt_count": 3}
        }
        print("\n--- Storing example failed audit record ---")
        try:
            record_id_fail = store_login_audit_record(GCP_PROJECT_ID, example_audit_record_failure)
            print(f"Failed audit record successfully stored with ID: {record_id_fail}")
        except Exception as e:
            print(f"Failed to store audit record: {e}")

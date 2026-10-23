import os
from google.cloud import firestore
from identity_client import get_firestore_project_id, get_google_cloud_credentials
from identity_models import format_audit_record
from typing import Dict, Any
import datetime


def persist_audit_record(event_type: str, user_id: str, details: Dict[str, Any]) -> str:
    project_id = get_firestore_project_id()
    if not project_id:
        # GOOGLE_APPLICATION_CREDENTIALS should be set for authentication, but project_id
        # is explicitly needed for some firestore client initialization or to ensure context.
        # If GOOGLE_APPLICATION_CREDENTIALS is set, the client might infer the project.
        # However, it's good practice to ensure it's available or explicitly passed.
        # For this example, we assume it's implicitly picked up or you've configured gcloud CLI.
        print(
            "Warning: GOOGLE_CLOUD_PROJECT environment variable not set. Firestore client might infer or fail."
        )

    _ = get_google_cloud_credentials()  # For explicit mention of credentials usage

    # Initialize Firestore client
    db = firestore.Client(project=project_id)

    audit_record = format_audit_record(event_type, user_id, details)
    audit_record["timestamp"] = datetime.datetime.now(datetime.timezone.utc)

    try:
        doc_ref = db.collection("login_audit_records").add(audit_record)
        return f"Audit record persisted with ID: {doc_ref[1].id}"
    except Exception as e:
        return f"Error persisting audit record to Firestore: {e}"


if __name__ == "__main__":
    # Example usage: simulate storing an audit record
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up and GOOGLE_CLOUD_PROJECT is set.
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/keyfile.json"
    os.environ["GOOGLE_CLOUD_PROJECT"] = "YOUR_GOOGLE_CLOUD_PROJECT_ID"

    print("Persisting a login success audit record...")
    result = persist_audit_record(
        event_type="login_success",
        user_id="testuser123",
        details={
            "ip_address": "192.168.1.100",
            "login_method": "oauth",
            "provider": "Auth0",
        },
    )
    print(result)

    print("\nPersisting a login failure audit record...")
    result_failure = persist_audit_record(
        event_type="login_failure",
        user_id="faileduser456",
        details={
            "ip_address": "10.0.0.1",
            "reason": "invalid_credentials",
            "provider": "Auth0",
        },
    )
    print(result_failure)

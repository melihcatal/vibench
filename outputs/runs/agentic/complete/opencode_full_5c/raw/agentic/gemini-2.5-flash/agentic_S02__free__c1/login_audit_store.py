import os
import datetime
from google.cloud import firestore  # Google Cloud Firestore SDK
from identity_models import AuditRecord

# Google Cloud Project ID
GOOGLE_PROJECT_ID = os.environ.get("GOOGLE_PROJECT_ID", "your-gcp-project-id")

# Firestore collection name for audit records
AUDIT_COLLECTION = "federated_login_audit"


def persist_audit_record(record: AuditRecord) -> str:
    db = firestore.Client(project=GOOGLE_PROJECT_ID)  # Google Cloud Firestore client

    # Convert AuditRecord to a dictionary for Firestore. Ensure timestamp is in a Firestore-compatible format.
    record_dict = {
        "timestamp": datetime.datetime.fromisoformat(
            record.timestamp.replace("Z", "+00:00")
        )
        if "Z" in record.timestamp
        else datetime.datetime.fromisoformat(record.timestamp),
        "event_type": record.event_type,
        "user_id": record.user_id,
        "provider": record.provider,
        "details": record.details,
    }

    # Add a new document to the 'federated_login_audit' collection
    doc_ref = db.collection(AUDIT_COLLECTION).add(record_dict)

    # Google Cloud Firestore SDK import: google.cloud.firestore
    return doc_ref[1].id  # Returns the ID of the newly created document


if __name__ == "__main__":
    # To run this example, ensure GOOGLE_PROJECT_ID is set in your environment
    # and you have authenticated your Google Cloud SDK (e.g., `gcloud auth application-default login`).
    # Also, ensure 'google-cloud-firestore' is installed: pip install google-cloud-firestore

    example_record = AuditRecord(
        timestamp=datetime.datetime.utcnow().isoformat() + "Z",
        event_type="login_success",
        user_id="user-123",
        provider="Google",
        details={
            "ip_address": "192.168.1.1",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        },
    )

    try:
        print(
            f"Persisting audit record to Google Cloud Firestore for project {GOOGLE_PROJECT_ID}..."
        )
        doc_id = persist_audit_record(example_record)
        print(f"Audit record successfully persisted with document ID: {doc_id}")
    except Exception as e:
        print(f"Error persisting audit record: {e}")
        print(
            "Please ensure 'google-cloud-firestore' is installed and you are authenticated to Google Cloud."
        )

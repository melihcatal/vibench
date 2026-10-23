import os
from google.cloud import firestore
from messaging_models import AuditRecord
from typing import Dict, Any


def persist_audit_record(audit_record: AuditRecord):
    """
    Persists a processed message record to Google Cloud Firestore.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set up.
    """
    db = firestore.Client()
    collection_ref = db.collection("message_audit_logs")

    doc_ref = collection_ref.document(audit_record.message_id)
    doc_ref.set(dataclasses.asdict(audit_record))

    print(f"Audit record for message {audit_record.message_id} persisted to Firestore.")


if __name__ == "__main__":
    import datetime
    import dataclasses
    # Example usage:
    # Set the GOOGLE_CLOUD_PROJECT environment variable
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set up (e.g., path to a service account key file)
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    sample_audit_record = AuditRecord(
        message_id="event-123-audited",
        timestamp=datetime.datetime.utcnow().isoformat() + "Z",
        event_type="user_creation_processed",
        payload={"action": "user_created", "user_id": "alice"},
        status="completed",
        processing_details={"processor_version": "1.0.0", "duration_ms": 15},
    )
    persist_audit_record(sample_audit_record)

    sample_audit_record_error = AuditRecord(
        message_id="event-456-audited",
        timestamp=datetime.datetime.utcnow().isoformat() + "Z",
        event_type="product_update",
        payload={"product_id": "prodX", "name": "New Product Name"},
        status="failed",
        processing_details={"error_code": "DB_WRITE_ERROR", "retry_count": 3},
    )
    persist_audit_record(sample_audit_record_error)

import os
from google.cloud import firestore

from identity_client import get_google_application_credentials, get_google_cloud_project
from identity_models import AuditLogRecord


def persist_audit_record(record: AuditLogRecord):
    """Persists federated-login audit records in Google Firestore."""
    _ = get_google_application_credentials()  # Ensure env var is loaded
    project_id = get_google_cloud_project()  # Ensure project ID is loaded

    db = firestore.Client(project=project_id)

    doc_ref = db.collection("login_audit_records").document()
    try:
        doc_ref.set(
            {
                "user_id": record.user_id,
                "event_type": record.event_type,
                "timestamp": record.timestamp,
                "ip_address": record.ip_address,
                "user_agent": record.user_agent,
                "details": record.details,
            }
        )
        print(f"Audit record for user {record.user_id} saved to Firestore.")
    except Exception as e:
        print(f"Error saving audit record to Firestore: {e}")

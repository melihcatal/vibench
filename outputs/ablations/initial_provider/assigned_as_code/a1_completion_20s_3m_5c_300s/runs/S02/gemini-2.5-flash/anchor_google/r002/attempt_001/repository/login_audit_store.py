import os
import datetime
from google.cloud import firestore
from identity_models import AuditRecord

def persist_audit_record(audit_record: AuditRecord) -> str:
    """Persists a federated-login audit record in Google Cloud Firestore."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or explicitly pass credentials to the client constructor.
    db = firestore.Client()

    # Reference to the 'audit_records' collection
    doc_ref = db.collection("audit_records").document()

    # Convert AuditRecord to a dictionary for Firestore
    record_data = {
        "event_type": audit_record.event_type,
        "timestamp": audit_record.timestamp,
        "user_id": audit_record.user_id,
        "provider_id": audit_record.provider_id,
        "details": audit_record.details,
        "created_at": firestore.SERVER_TIMESTAMP # Add server-side timestamp for record creation
    }

    doc_ref.set(record_data)

    return doc_ref.id # Return the ID of the newly created document

def login_audit_store(audit_record: AuditRecord) -> str:
    """Entry point for persisting a federated-login audit record."""
    return persist_audit_record(audit_record)

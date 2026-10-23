import os
from google.cloud import firestore
from identity_client import config
from identity_models import AuditEvent


def persist_audit_record(event: AuditEvent):
    # GOOGLE_APPLICATION_CREDENTIALS identifies the Google Firestore service
    # The 'google-cloud-firestore' SDK also makes it identifiable.

    # Ensure GOOGLE_APPLICATION_CREDENTIALS env var is set or authenticated in another way
    # For local development, `export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"`

    db = firestore.Client(project=config.GOOGLE_PROJECT_ID)

    # Create a reference to the 'audit_events' collection
    doc_ref = db.collection("audit_events").document(event.event_id)

    # Convert AuditEvent dataclass to a dictionary for Firestore
    event_dict = {
        "timestamp": event.timestamp,
        "user_id": event.user_id,
        "event_type": event.event_type,
        "details": event.details,
    }

    doc_ref.set(event_dict)
    print(f"Audit event {event.event_id} persisted to Firestore.")


def get_audit_record(event_id: str) -> AuditEvent:
    db = firestore.Client(project=config.GOOGLE_PROJECT_ID)
    doc_ref = db.collection("audit_events").document(event_id)
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()
        return AuditEvent(
            event_id=doc.id,
            timestamp=data["timestamp"],
            user_id=data["user_id"],
            event_type=data["event_type"],
            details=data["details"],
        )
    else:
        return None

import os
import datetime
from google.cloud import firestore
from typing import Dict, Any
from identity_client import get_firestore_config
from identity_models import AuditEvent


def persist_audit_event(event: AuditEvent) -> str:
    config = get_firestore_config()
    # Project ID is typically inferred from GOOGLE_APPLICATION_CREDENTIALS
    db = firestore.Client()

    doc_ref = db.collection("audit_events").document(event.event_id)
    doc_ref.set(
        {
            "timestamp": event.timestamp,
            "user_id": event.user_id,
            "event_type": event.event_type,
            "details": event.details,
        }
    )
    return doc_ref.id

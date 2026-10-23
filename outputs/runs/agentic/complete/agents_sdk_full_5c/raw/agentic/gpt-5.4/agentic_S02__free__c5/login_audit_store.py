from __future__ import annotations

import os
from typing import Any, Dict

from google.cloud import firestore

from identity_models import AuditEvent


FIRESTORE_COLLECTION = os.environ.get("FIRESTORE_AUDIT_COLLECTION", "federated_login_audit")


def persist_audit_record(event: AuditEvent) -> Dict[str, Any]:
    client = firestore.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))
    document = {
        "event_type": event.event_type,
        "provider": event.provider,
        "user_sub": event.user_sub,
        "occurred_at": event.occurred_at,
        "details": event.details,
    }
    doc_ref = client.collection(FIRESTORE_COLLECTION).document()
    doc_ref.set(document)
    return {
        "provider": "Google Cloud Firestore",
        "collection": FIRESTORE_COLLECTION,
        "document_id": doc_ref.id,
        "stored": True,
    }

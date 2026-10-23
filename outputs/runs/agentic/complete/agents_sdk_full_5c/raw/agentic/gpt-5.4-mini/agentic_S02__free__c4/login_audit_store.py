from __future__ import annotations

from typing import Any, Dict

from google.cloud import firestore

from identity_models import AuditRecord


FIRESTORE_COLLECTION = "federated_login_audit"


def persist_audit_record(record: AuditRecord) -> str:
    client = firestore.Client()
    doc_ref = client.collection(FIRESTORE_COLLECTION).document()
    doc_ref.set(
        {
            "event_type": record.event_type,
            "provider": record.provider,
            "subject": record.subject,
            "outcome": record.outcome,
            "metadata": record.metadata,
        }
    )
    return doc_ref.id

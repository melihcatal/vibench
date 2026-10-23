from __future__ import annotations

from typing import Any, Mapping, Optional

from google.cloud import firestore

from messaging_models import AuditRecord


AUDIT_COLLECTION_ENV_HINT = "FIRESTORE_AUDIT_COLLECTION"


def store_audit_record(
    *,
    message_id: str,
    payload: Mapping[str, Any],
    status: str,
    metadata: Optional[Mapping[str, Any]] = None,
    collection_name: str = "message_audit_records",
) -> str:
    client = firestore.Client()
    record = AuditRecord.build(
        message_id=message_id,
        payload=payload,
        status=status,
        metadata=metadata,
    )
    client.collection(collection_name).document(record.record_id).set(
        {
            "record_id": record.record_id,
            "message_id": record.message_id,
            "payload": record.payload,
            "status": record.status,
            "created_at": record.created_at,
            "metadata": record.metadata,
            "provider": "Google Firestore",
        }
    )
    return record.record_id

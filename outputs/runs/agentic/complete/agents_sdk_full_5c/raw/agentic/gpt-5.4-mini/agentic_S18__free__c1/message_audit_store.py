from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping

from google.cloud import firestore

from messaging_models import AuditRecord, normalize_attributes, normalize_payload


def store_audit_record(record_id: str, message_id: str, status: str, payload: Any, attributes: Mapping[str, Any]) -> AuditRecord:
    client = firestore.Client()
    collection = client.collection("message_audit")
    record = AuditRecord(
        record_id=record_id,
        message_id=message_id,
        status=status,
        payload=normalize_payload(payload),
        attributes=normalize_attributes(attributes),
        stored_at=datetime.now(timezone.utc).isoformat(),
    )
    collection.document(record_id).set(
        {
            "record_id": record.record_id,
            "message_id": record.message_id,
            "status": record.status,
            "payload": record.payload,
            "attributes": record.attributes,
            "stored_at": record.stored_at,
        }
    )
    return record

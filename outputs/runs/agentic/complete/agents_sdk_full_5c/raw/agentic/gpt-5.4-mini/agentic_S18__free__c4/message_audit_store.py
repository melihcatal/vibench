import json
from datetime import datetime, timezone
from typing import Mapping

from google.cloud import firestore

from messaging_models import AuditRecord


def store_audit_record(message_id: str, status: str, summary: str, metadata: Mapping[str, object]) -> str:
    client = firestore.Client()
    record = AuditRecord(
        message_id=message_id,
        processed_at=datetime.now(timezone.utc).isoformat(),
        status=status,
        summary=summary,
        metadata=dict(metadata),
    )
    doc = client.collection("message_audit").document(message_id)
    doc.set({
        "message_id": record.message_id,
        "processed_at": record.processed_at,
        "status": record.status,
        "summary": record.summary,
        "metadata": record.metadata,
    })
    return message_id

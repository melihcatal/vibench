from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Iterable

from google.cloud import firestore

from messaging_models import MessageAuditRecord

FIRESTORE_COLLECTION = os.getenv("FIRESTORE_AUDIT_COLLECTION", "message_audit")


def persist_audit_record(record: MessageAuditRecord, project_id: str | None = None) -> str:
    client = firestore.Client(project=project_id)
    doc = client.collection(FIRESTORE_COLLECTION).document(record.message_id)
    doc.set(
        {
            "message_id": record.message_id,
            "status": record.status,
            "processed_at": record.processed_at,
            "summary": record.summary,
            "attributes": record.attributes,
            "stored_at": datetime.now(timezone.utc).isoformat(),
        }
    )
    return doc.id

from datetime import datetime, timezone
from typing import Any, Dict

from google.cloud import firestore

from database_client import document_ref, normalize_for_firestore
from database_models import (
    ConditionalUpdateResult,
    normalize_document_id,
    normalize_payload,
)


def conditional_update(
    document_id: Any, updates: Dict[str, Any], expected_version: int
) -> ConditionalUpdateResult:
    doc_id = normalize_document_id(document_id)
    payload = normalize_for_firestore(normalize_payload(updates))
    ref = document_ref(doc_id)
    transaction = firestore.Transaction()
    snapshot = ref.get(transaction=transaction)
    if not snapshot.exists:
        return ConditionalUpdateResult(
            document_id=doc_id, updated=False, version=None, data={}
        )
    current_version = int(snapshot.get("version", 0))
    if current_version != int(expected_version):
        return ConditionalUpdateResult(
            document_id=doc_id,
            updated=False,
            version=current_version,
            data=snapshot.to_dict() or {},
        )
    payload["version"] = current_version + 1
    payload["updated_at"] = datetime.now(timezone.utc)
    ref.set(payload, merge=True)
    merged = snapshot.to_dict() or {}
    merged.update(payload)
    merged["id"] = doc_id
    return ConditionalUpdateResult(
        document_id=doc_id, updated=True, version=current_version + 1, data=merged
    )

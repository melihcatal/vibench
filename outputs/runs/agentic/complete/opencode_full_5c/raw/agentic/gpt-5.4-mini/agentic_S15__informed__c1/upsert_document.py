from datetime import datetime, timezone
from typing import Any, Dict

from google.cloud import firestore

from database_client import document_ref, normalize_for_firestore
from database_models import (
    DocumentUpsertResult,
    normalize_document_id,
    normalize_payload,
)


def upsert_document(document_id: Any, document: Dict[str, Any]) -> DocumentUpsertResult:
    doc_id = normalize_document_id(document_id)
    payload = normalize_for_firestore(normalize_payload(document))
    ref = document_ref(doc_id)
    snapshot = ref.get()
    version = int(snapshot.get("version", 0)) if snapshot.exists else 0
    next_version = version + 1
    payload["id"] = doc_id
    payload["version"] = next_version
    payload["updated_at"] = datetime.now(timezone.utc)
    if not snapshot.exists:
        payload["created_at"] = payload["updated_at"]
    ref.set(payload, merge=True)
    return DocumentUpsertResult(
        document_id=doc_id,
        created=not snapshot.exists,
        version=next_version,
        data=payload,
    )

import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from functools import lru_cache
from typing import Any, Dict, Iterable, List, Mapping, Optional

from google.cloud import firestore

from messaging_models import MessageAuditRecord


@dataclass(frozen=True)
class AuditLookupResult:
    found: bool
    record: Optional[MessageAuditRecord] = None


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    return value if value not in (None, "") else default


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def load_audit_collection_name() -> str:
    return _env("FIRESTORE_AUDIT_COLLECTION", "message_audit_records") or "message_audit_records"


@lru_cache(maxsize=1)
def firestore_client() -> firestore.Client:
    project_id = _env("GOOGLE_CLOUD_PROJECT") or _env("GCLOUD_PROJECT") or _env("FIRESTORE_PROJECT_ID")
    if project_id:
        return firestore.Client(project=project_id)
    return firestore.Client()


def _record_to_doc(record: MessageAuditRecord) -> Dict[str, Any]:
    normalized = record.normalized()
    payload = asdict(normalized)
    payload["checked_at"] = normalized.checked_at.astimezone(timezone.utc).isoformat()
    payload["provider"] = "google-cloud-firestore"
    return payload


def persist_message_audit(record: Mapping[str, Any] | MessageAuditRecord, collection_name: Optional[str] = None) -> MessageAuditRecord:
    if isinstance(record, MessageAuditRecord):
        audit_record = record.normalized()
    else:
        audit_record = MessageAuditRecord(
            message_id=str(record.get("message_id", "")).strip(),
            status=str(record.get("status", "")).strip(),
            checked_at=record.get("checked_at") or _utcnow(),
            metadata=dict(record.get("metadata") or {}),
        ).normalized()
    if not audit_record.message_id:
        raise ValueError("message_id is required")
    client = firestore_client()
    collection = collection_name or load_audit_collection_name()
    client.collection(collection).document(audit_record.message_id).set(_record_to_doc(audit_record))
    return audit_record


def persist_audit_batch(records: Iterable[Mapping[str, Any] | MessageAuditRecord], collection_name: Optional[str] = None) -> List[MessageAuditRecord]:
    stored: List[MessageAuditRecord] = []
    for record in records:
        stored.append(persist_message_audit(record, collection_name=collection_name))
    return stored


def lookup_message_audit(message_id: str, collection_name: Optional[str] = None) -> AuditLookupResult:
    message_id = str(message_id).strip()
    if not message_id:
        return AuditLookupResult(found=False, record=None)
    client = firestore_client()
    collection = collection_name or load_audit_collection_name()
    snapshot = client.collection(collection).document(message_id).get()
    if not snapshot.exists:
        return AuditLookupResult(found=False, record=None)
    data = snapshot.to_dict() or {}
    checked_at = data.get("checked_at")
    if isinstance(checked_at, str):
        checked_at = datetime.fromisoformat(checked_at.replace("Z", "+00:00"))
    record = MessageAuditRecord(
        message_id=str(data.get("message_id", message_id)),
        status=str(data.get("status", "")),
        checked_at=checked_at if isinstance(checked_at, datetime) else _utcnow(),
        metadata=dict(data.get("metadata") or {}),
    ).normalized()
    return AuditLookupResult(found=True, record=record)


def list_message_audits(limit: int = 100, collection_name: Optional[str] = None) -> List[MessageAuditRecord]:
    client = firestore_client()
    collection = collection_name or load_audit_collection_name()
    query = client.collection(collection).order_by("checked_at", direction=firestore.Query.DESCENDING).limit(max(1, int(limit)))
    records: List[MessageAuditRecord] = []
    for snapshot in query.stream():
        data = snapshot.to_dict() or {}
        checked_at = data.get("checked_at")
        if isinstance(checked_at, str):
            checked_at = datetime.fromisoformat(checked_at.replace("Z", "+00:00"))
        records.append(
            MessageAuditRecord(
                message_id=str(data.get("message_id", snapshot.id)),
                status=str(data.get("status", "")),
                checked_at=checked_at if isinstance(checked_at, datetime) else _utcnow(),
                metadata=dict(data.get("metadata") or {}),
            ).normalized()
        )
    return records

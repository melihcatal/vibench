import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Mapping, Optional

from google.cloud import firestore


GCP_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"
FIRESTORE_COLLECTION_ENV = "LOGIN_AUDIT_COLLECTION"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _coerce_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _coerce_bool(value: Any) -> Optional[bool]:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "f", "no", "n", "off"}:
        return False
    return None


def _coerce_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_dict(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return dict(value)
    try:
        return dict(value)
    except Exception:
        return {"value": value}


@dataclass(frozen=True)
class LoginAuditRecord:
    event_type: str
    provider: str
    subject: Optional[str] = None
    client_id: Optional[str] = None
    issuer: Optional[str] = None
    request_id: Optional[str] = None
    session_id: Optional[str] = None
    success: Optional[bool] = None
    error: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    latency_ms: Optional[int] = None
    claims: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    occurred_at: datetime = field(default_factory=_utc_now)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "LoginAuditRecord":
        event_type = _coerce_str(data.get("event_type") or data.get("eventType"))
        provider = _coerce_str(data.get("provider") or data.get("issuer"))
        if not event_type:
            raise ValueError("event_type is required")
        if not provider:
            raise ValueError("provider is required")
        occurred_at = data.get("occurred_at") or data.get("occurredAt")
        parsed_occurred_at = occurred_at if isinstance(occurred_at, datetime) else _utc_now()
        return cls(
            event_type=event_type,
            provider=provider,
            subject=_coerce_str(data.get("subject") or data.get("sub")),
            client_id=_coerce_str(data.get("client_id") or data.get("clientId")),
            issuer=_coerce_str(data.get("issuer") or data.get("iss")),
            request_id=_coerce_str(data.get("request_id") or data.get("requestId")),
            session_id=_coerce_str(data.get("session_id") or data.get("sessionId")),
            success=_coerce_bool(data.get("success")),
            error=_coerce_str(data.get("error")),
            ip_address=_coerce_str(data.get("ip_address") or data.get("ipAddress")),
            user_agent=_coerce_str(data.get("user_agent") or data.get("userAgent")),
            latency_ms=_coerce_int(data.get("latency_ms") or data.get("latencyMs")),
            claims=_as_dict(data.get("claims")),
            metadata=_as_dict(data.get("metadata")),
            occurred_at=parsed_occurred_at,
        )

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "event_type": self.event_type,
            "provider": self.provider,
            "occurred_at": self.occurred_at.isoformat(),
        }
        for key in (
            "subject",
            "client_id",
            "issuer",
            "request_id",
            "session_id",
            "success",
            "error",
            "ip_address",
            "user_agent",
            "latency_ms",
        ):
            value = getattr(self, key)
            if value is not None:
                payload[key] = value
        if self.claims:
            payload["claims"] = dict(self.claims)
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


class FirestoreLoginAuditStore:
    def __init__(self, project_id: Optional[str] = None, collection_name: Optional[str] = None, client: Optional[Any] = None):
        self.project_id = project_id or os.getenv(GCP_PROJECT_ENV)
        self.collection_name = collection_name or os.getenv(FIRESTORE_COLLECTION_ENV, "login_audit_events")
        self._client = client or firestore.Client(project=self.project_id)

    @property
    def client(self) -> Any:
        return self._client

    def save(self, record: Mapping[str, Any] | LoginAuditRecord) -> str:
        normalized = record if isinstance(record, LoginAuditRecord) else LoginAuditRecord.from_dict(record)
        doc_ref = self.client.collection(self.collection_name).document()
        doc_ref.set(normalized.to_dict())
        return doc_ref.id

    def fetch(self, document_id: str) -> Dict[str, Any]:
        snapshot = self.client.collection(self.collection_name).document(document_id).get()
        if not snapshot.exists:
            raise KeyError(document_id)
        data = snapshot.to_dict() or {}
        data["id"] = snapshot.id
        return data

    def query_by_subject(self, subject: str, limit: int = 50) -> list[Dict[str, Any]]:
        results = []
        query = self.client.collection(self.collection_name).where("subject", "==", subject).limit(limit)
        for snapshot in query.stream():
            item = snapshot.to_dict() or {}
            item["id"] = snapshot.id
            results.append(item)
        return results

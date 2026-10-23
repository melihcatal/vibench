from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import os
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence

from azure.cosmos import CosmosClient, PartitionKey


def _clean_str(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        return value or None
    return str(value).strip() or None


def _to_datetime(value: Any) -> Optional[datetime]:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    text = str(value).strip()
    try:
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        parsed = datetime.fromisoformat(text)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class LoginAuditRecord:
    event_type: str
    user_id: Optional[str] = None
    provider: Optional[str] = None
    client_id: Optional[str] = None
    session_id: Optional[str] = None
    ip_address: Optional[str] = None
    success: Optional[bool] = None
    timestamp: datetime = field(default_factory=_utc_now)
    details: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "LoginAuditRecord":
        return cls(
            event_type=_clean_str(data.get("event_type") or data.get("type") or data.get("event")) or "unknown",
            user_id=_clean_str(data.get("user_id") or data.get("sub") or data.get("user")),
            provider=_clean_str(data.get("provider") or data.get("connection") or data.get("issuer")),
            client_id=_clean_str(data.get("client_id") or data.get("audience")),
            session_id=_clean_str(data.get("session_id") or data.get("sid") or data.get("state")),
            ip_address=_clean_str(data.get("ip_address") or data.get("ip") or data.get("origin_ip")),
            success=_to_bool(data.get("success") if "success" in data else data.get("status")),
            timestamp=_to_datetime(data.get("timestamp") or data.get("created_at") or data.get("date")) or _utc_now(),
            details=dict(data),
        )

    def to_document(self) -> Dict[str, Any]:
        document: Dict[str, Any] = {
            "id": self.document_id,
            "partitionKey": self.partition_key,
            "event_type": self.event_type,
            "timestamp": self.timestamp.astimezone(timezone.utc).isoformat(),
            "details": dict(self.details),
        }
        if self.user_id is not None:
            document["user_id"] = self.user_id
        if self.provider is not None:
            document["provider"] = self.provider
        if self.client_id is not None:
            document["client_id"] = self.client_id
        if self.session_id is not None:
            document["session_id"] = self.session_id
        if self.ip_address is not None:
            document["ip_address"] = self.ip_address
        if self.success is not None:
            document["success"] = self.success
        return document

    @property
    def partition_key(self) -> str:
        return self.provider or self.client_id or "unknown"

    @property
    def document_id(self) -> str:
        timestamp = self.timestamp.astimezone(timezone.utc).isoformat()
        basis = "|".join(
            [
                self.event_type,
                self.user_id or "",
                self.provider or "",
                self.client_id or "",
                self.session_id or "",
                timestamp,
            ]
        )
        return basis.replace(" ", "_")


def _to_bool(value: Any) -> Optional[bool]:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"true", "1", "yes", "y", "on", "success", "ok"}:
        return True
    if text in {"false", "0", "no", "n", "off", "failure", "failed", "error"}:
        return False
    return None


@dataclass(frozen=True)
class CosmosLoginAuditStoreConfig:
    endpoint: str
    key: str
    database_name: str
    container_name: str


def load_cosmos_login_audit_store_config(prefix: str = "COSMOS_LOGIN_AUDIT_") -> CosmosLoginAuditStoreConfig:
    return CosmosLoginAuditStoreConfig(
        endpoint=os.environ[f"{prefix}ENDPOINT"],
        key=os.environ[f"{prefix}KEY"],
        database_name=os.environ.get(f"{prefix}DATABASE", "identity_audit"),
        container_name=os.environ.get(f"{prefix}CONTAINER", "login_events"),
    )


class CosmosLoginAuditStore:
    def __init__(self, config: CosmosLoginAuditStoreConfig):
        self._client = CosmosClient(config.endpoint, credential=config.key)
        self._database = self._client.create_database_if_not_exists(id=config.database_name)
        self._container = self._database.create_container_if_not_exists(
            id=config.container_name,
            partition_key=PartitionKey(path="/partitionKey"),
            offer_throughput=400,
        )

    def persist_record(self, record: LoginAuditRecord) -> Dict[str, Any]:
        return self._container.upsert_item(record.to_document())

    def persist_records(self, records: Sequence[LoginAuditRecord]) -> List[Dict[str, Any]]:
        return [self.persist_record(record) for record in records]

    def persist_mapping(self, data: Mapping[str, Any]) -> Dict[str, Any]:
        return self.persist_record(LoginAuditRecord.from_mapping(data))


def build_cosmos_login_audit_store_from_env() -> CosmosLoginAuditStore:
    return CosmosLoginAuditStore(load_cosmos_login_audit_store_config())

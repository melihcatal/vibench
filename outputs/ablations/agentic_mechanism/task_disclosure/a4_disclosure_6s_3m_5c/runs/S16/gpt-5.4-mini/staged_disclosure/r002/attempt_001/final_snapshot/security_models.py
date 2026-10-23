from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Optional
import base64
import json


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_secret_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("ascii")
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, separators=(",", ":"), sort_keys=True)
    return str(value)


def _normalize_secret_name(name: Any) -> str:
    normalized = str(name or "").strip()
    if not normalized:
        raise ValueError("secret name is required")
    return normalized


def _normalize_metadata(metadata: Optional[Mapping[str, Any]]) -> dict[str, str]:
    if not metadata:
        return {}
    return {str(k): _normalize_secret_value(v) for k, v in metadata.items()}


@dataclass(frozen=True)
class SecretCreateRequest:
    name: str
    value: str
    metadata: dict[str, str] = field(default_factory=dict)
    ttl_seconds: Optional[int] = None

    @classmethod
    def from_input(
        cls,
        name: Any,
        value: Any,
        metadata: Optional[Mapping[str, Any]] = None,
        ttl_seconds: Optional[Any] = None,
    ) -> "SecretCreateRequest":
        ttl = None if ttl_seconds is None else int(ttl_seconds)
        if ttl is not None and ttl <= 0:
            raise ValueError("ttl_seconds must be positive")
        return cls(
            name=_normalize_secret_name(name),
            value=_normalize_secret_value(value),
            metadata=_normalize_metadata(metadata),
            ttl_seconds=ttl,
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"name": self.name, "value": self.value}
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        if self.ttl_seconds is not None:
            payload["ttl_seconds"] = self.ttl_seconds
        return payload


@dataclass(frozen=True)
class SecretUpdateRequest:
    value: Optional[str] = None
    metadata: Optional[dict[str, str]] = None
    ttl_seconds: Optional[int] = None

    @classmethod
    def from_input(
        cls,
        value: Any = None,
        metadata: Optional[Mapping[str, Any]] = None,
        ttl_seconds: Optional[Any] = None,
    ) -> "SecretUpdateRequest":
        ttl = None if ttl_seconds is None else int(ttl_seconds)
        if ttl is not None and ttl <= 0:
            raise ValueError("ttl_seconds must be positive")
        normalized_metadata = None if metadata is None else _normalize_metadata(metadata)
        return cls(
            value=None if value is None else _normalize_secret_value(value),
            metadata=normalized_metadata,
            ttl_seconds=ttl,
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        if self.value is not None:
            payload["value"] = self.value
        if self.metadata is not None:
            payload["metadata"] = dict(self.metadata)
        if self.ttl_seconds is not None:
            payload["ttl_seconds"] = self.ttl_seconds
        return payload


@dataclass(frozen=True)
class SecretResponse:
    name: str
    value: str
    metadata: dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_now_utc)
    updated_at: datetime = field(default_factory=_now_utc)
    expires_at: Optional[datetime] = None
    version: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SecretResponse":
        created_at = data.get("created_at")
        updated_at = data.get("updated_at")
        expires_at = data.get("expires_at")
        return cls(
            name=_normalize_secret_name(data.get("name")),
            value=_normalize_secret_value(data.get("value")),
            metadata=_normalize_metadata(data.get("metadata")),
            created_at=_parse_datetime(created_at) if created_at else _now_utc(),
            updated_at=_parse_datetime(updated_at) if updated_at else _now_utc(),
            expires_at=_parse_datetime(expires_at) if expires_at else None,
            version=None if data.get("version") is None else str(data.get("version")),
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "name": self.name,
            "value": self.value,
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
        if self.expires_at is not None:
            payload["expires_at"] = self.expires_at.isoformat()
        if self.version is not None:
            payload["version"] = self.version
        return payload


def _parse_datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc) if value.tzinfo else value.replace(tzinfo=timezone.utc)
    text = str(value).replace("Z", "+00:00")
    parsed = datetime.fromisoformat(text)
    return parsed.astimezone(timezone.utc) if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)

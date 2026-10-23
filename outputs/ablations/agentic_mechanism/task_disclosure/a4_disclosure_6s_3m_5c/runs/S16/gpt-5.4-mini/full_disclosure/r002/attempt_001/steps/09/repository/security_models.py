from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional


def _coerce_str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    if isinstance(value, str):
        return value
    return str(value)


def _coerce_int(value: Any, default: int = 0) -> int:
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def _coerce_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "y", "on"}:
            return True
        if normalized in {"0", "false", "no", "n", "off"}:
            return False
    return default


@dataclass(frozen=True)
class SecretRequest:
    secret_id: str
    version_id: Optional[str] = None
    stage: Optional[str] = None
    project_id: Optional[str] = None
    region: Optional[str] = None

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "SecretRequest":
        return cls(
            secret_id=_coerce_str(data.get("secret_id")),
            version_id=data.get("version_id"),
            stage=data.get("stage"),
            project_id=data.get("project_id"),
            region=data.get("region"),
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {"secret_id": self.secret_id}
        if self.version_id is not None:
            payload["version_id"] = self.version_id
        if self.stage is not None:
            payload["stage"] = self.stage
        if self.project_id is not None:
            payload["project_id"] = self.project_id
        if self.region is not None:
            payload["region"] = self.region
        return payload


@dataclass(frozen=True)
class SecretResponse:
    secret_id: str
    value: str
    version_id: Optional[str] = None
    stage: Optional[str] = None
    created_at: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "SecretResponse":
        return cls(
            secret_id=_coerce_str(data.get("secret_id")),
            value=_coerce_str(data.get("value")),
            version_id=data.get("version_id"),
            stage=data.get("stage"),
            created_at=data.get("created_at"),
            content_type=data.get("content_type"),
            metadata=dict(data.get("metadata") or {}),
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "secret_id": self.secret_id,
            "value": self.value,
            "metadata": dict(self.metadata),
        }
        if self.version_id is not None:
            payload["version_id"] = self.version_id
        if self.stage is not None:
            payload["stage"] = self.stage
        if self.created_at is not None:
            payload["created_at"] = self.created_at
        if self.content_type is not None:
            payload["content_type"] = self.content_type
        return payload


@dataclass(frozen=True)
class NormalizedSecret:
    secret_id: str
    value: str
    version_id: Optional[str] = None
    stage: Optional[str] = None
    content_type: Optional[str] = None
    is_binary: bool = False
    labels: tuple[str, ...] = ()

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "NormalizedSecret":
        labels = data.get("labels") or ()
        if isinstance(labels, str):
            labels = (labels,)
        return cls(
            secret_id=_coerce_str(data.get("secret_id")),
            value=_coerce_str(data.get("value")),
            version_id=data.get("version_id"),
            stage=data.get("stage"),
            content_type=data.get("content_type"),
            is_binary=_coerce_bool(data.get("is_binary")),
            labels=tuple(_coerce_str(label) for label in labels if _coerce_str(label)),
        )

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "secret_id": self.secret_id,
            "value": self.value,
            "is_binary": self.is_binary,
            "labels": list(self.labels),
        }
        if self.version_id is not None:
            payload["version_id"] = self.version_id
        if self.stage is not None:
            payload["stage"] = self.stage
        if self.content_type is not None:
            payload["content_type"] = self.content_type
        return payload


def normalize_secret_payload(payload: Mapping[str, Any]) -> NormalizedSecret:
    return NormalizedSecret.from_mapping(payload)


def normalize_secret_request(payload: Mapping[str, Any]) -> SecretRequest:
    return SecretRequest.from_mapping(payload)


def normalize_secret_response(payload: Mapping[str, Any]) -> SecretResponse:
    return SecretResponse.from_mapping(payload)


def normalize_secret_value(value: Any) -> str:
    return _coerce_str(value)


def normalize_secret_version(version: Any) -> Optional[str]:
    if version is None:
        return None
    text = _coerce_str(version).strip()
    return text or None


def normalize_secret_stage(stage: Any) -> Optional[str]:
    if stage is None:
        return None
    text = _coerce_str(stage).strip()
    return text or None

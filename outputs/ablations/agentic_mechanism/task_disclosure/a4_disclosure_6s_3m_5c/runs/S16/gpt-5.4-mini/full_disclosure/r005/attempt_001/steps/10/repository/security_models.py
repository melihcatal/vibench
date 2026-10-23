from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional


def _as_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def _strip_or_none(value: Any) -> Optional[str]:
    text = _as_str(value).strip()
    return text or None


def normalize_secret_payload(payload: Any) -> dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, Mapping):
        return dict(payload)
    if hasattr(payload, "model_dump"):
        return dict(payload.model_dump())
    if hasattr(payload, "dict"):
        return dict(payload.dict())
    return {"value": payload}


@dataclass(slots=True)
class SecretRequest:
    secret_id: str
    version: Optional[str] = None
    stage: Optional[str] = None
    project_id: Optional[str] = None
    region: Optional[str] = None

    def normalized(self) -> "SecretRequest":
        return SecretRequest(
            secret_id=_as_str(self.secret_id).strip(),
            version=_strip_or_none(self.version),
            stage=_strip_or_none(self.stage),
            project_id=_strip_or_none(self.project_id),
            region=_strip_or_none(self.region),
        )


@dataclass(slots=True)
class SecretResponse:
    secret_id: str
    value: Any = None
    version: Optional[str] = None
    stage: Optional[str] = None
    payload: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, secret_id: str, payload: Any) -> "SecretResponse":
        normalized = normalize_secret_payload(payload)
        value = normalized.get("value")
        version = _strip_or_none(normalized.get("version") or normalized.get("version_id"))
        stage = _strip_or_none(normalized.get("stage") or normalized.get("version_stage"))
        return cls(
            secret_id=_as_str(secret_id).strip(),
            value=value,
            version=version,
            stage=stage,
            payload=normalized,
        )


@dataclass(slots=True)
class SecretNormalizationResult:
    secret_id: str
    raw_value: Any = None
    normalized_value: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_value(cls, secret_id: str, value: Any, metadata: Optional[Mapping[str, Any]] = None) -> "SecretNormalizationResult":
        normalized_value = _strip_or_none(value)
        return cls(
            secret_id=_as_str(secret_id).strip(),
            raw_value=value,
            normalized_value=normalized_value,
            metadata=dict(metadata or {}),
        )

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Mapping, Optional


class SecretValueFormat(str, Enum):
    TEXT = "text"
    JSON = "json"
    BYTES = "bytes"


@dataclass(frozen=True)
class SecretReference:
    name: str
    version: Optional[str] = None
    stage: Optional[str] = None

    def normalize(self) -> "SecretReference":
        return SecretReference(
            name=self.name.strip(),
            version=self.version.strip() if isinstance(self.version, str) and self.version.strip() else None,
            stage=self.stage.strip() if isinstance(self.stage, str) and self.stage.strip() else None,
        )


@dataclass(frozen=True)
class SecretFetchRequest:
    secret: SecretReference
    format: SecretValueFormat = SecretValueFormat.TEXT
    timeout_seconds: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalize(self) -> "SecretFetchRequest":
        return SecretFetchRequest(
            secret=self.secret.normalize(),
            format=SecretValueFormat(self.format.value if isinstance(self.format, SecretValueFormat) else str(self.format)),
            timeout_seconds=self.timeout_seconds,
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True)
class SecretVersionInfo:
    version: Optional[str] = None
    stage: Optional[str] = None
    created_at: Optional[datetime] = None

    def normalize(self) -> "SecretVersionInfo":
        created_at = self.created_at
        if created_at is not None and created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        return SecretVersionInfo(
            version=self.version.strip() if isinstance(self.version, str) and self.version.strip() else None,
            stage=self.stage.strip() if isinstance(self.stage, str) and self.stage.strip() else None,
            created_at=created_at,
        )


@dataclass(frozen=True)
class SecretFetchResponse:
    secret: SecretReference
    value: Any
    format: SecretValueFormat = SecretValueFormat.TEXT
    version_info: Optional[SecretVersionInfo] = None
    retrieved_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalize(self) -> "SecretFetchResponse":
        version_info = self.version_info.normalize() if self.version_info else None
        retrieved_at = self.retrieved_at
        if retrieved_at.tzinfo is None:
            retrieved_at = retrieved_at.replace(tzinfo=timezone.utc)
        return SecretFetchResponse(
            secret=self.secret.normalize(),
            value=self.value,
            format=SecretValueFormat(self.format.value if isinstance(self.format, SecretValueFormat) else str(self.format)),
            version_info=version_info,
            retrieved_at=retrieved_at,
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True)
class SecretNormalizationResult:
    original: Any
    normalized: Any
    changed: bool
    issues: tuple[str, ...] = ()


def normalize_secret_name(name: str) -> str:
    return name.strip()


def normalize_stage(stage: Optional[str]) -> Optional[str]:
    if stage is None:
        return None
    normalized = stage.strip()
    return normalized or None


def normalize_secret_payload(payload: Any) -> SecretNormalizationResult:
    issues = []
    normalized = payload
    if isinstance(payload, str):
        normalized = payload.strip()
    elif isinstance(payload, Mapping):
        normalized = dict(payload)
    elif isinstance(payload, bytes):
        normalized = payload
    else:
        issues.append("unsupported_payload_type")
    return SecretNormalizationResult(original=payload, normalized=normalized, changed=normalized != payload, issues=tuple(issues))


def coerce_secret_reference(value: Any) -> SecretReference:
    if isinstance(value, SecretReference):
        return value.normalize()
    if isinstance(value, Mapping):
        return SecretReference(
            name=str(value.get("name", "")).strip(),
            version=value.get("version"),
            stage=value.get("stage"),
        ).normalize()
    return SecretReference(name=str(value).strip()).normalize()


def coerce_fetch_request(value: Any) -> SecretFetchRequest:
    if isinstance(value, SecretFetchRequest):
        return value.normalize()
    if isinstance(value, Mapping):
        secret_value = value.get("secret", value.get("name", ""))
        return SecretFetchRequest(
            secret=coerce_secret_reference(secret_value),
            format=SecretValueFormat(str(value.get("format", SecretValueFormat.TEXT.value))),
            timeout_seconds=value.get("timeout_seconds"),
            metadata=dict(value.get("metadata", {})),
        ).normalize()
    return SecretFetchRequest(secret=coerce_secret_reference(value)).normalize()


def build_secret_fetch_response(secret: Any, value: Any, **kwargs: Any) -> SecretFetchResponse:
    response = SecretFetchResponse(
        secret=coerce_secret_reference(secret),
        value=value,
        format=SecretValueFormat(str(kwargs.get("format", SecretValueFormat.TEXT.value))),
        version_info=kwargs.get("version_info"),
        retrieved_at=kwargs.get("retrieved_at", datetime.now(timezone.utc)),
        metadata=dict(kwargs.get("metadata", {})),
    )
    return response.normalize()

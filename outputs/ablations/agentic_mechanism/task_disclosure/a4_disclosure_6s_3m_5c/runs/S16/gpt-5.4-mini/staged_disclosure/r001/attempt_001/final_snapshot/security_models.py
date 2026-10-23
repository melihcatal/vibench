from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, MutableMapping
import base64
import json
import os
import re


_SECRET_KEYS = (
    "secret",
    "token",
    "password",
    "passphrase",
    "api_key",
    "apikey",
    "client_secret",
    "private_key",
    "credential",
)


def _is_secret_key(key: str) -> bool:
    lowered = key.strip().lower()
    return any(marker in lowered for marker in _SECRET_KEYS)


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _normalize_secret_value(value: Any) -> str:
    text = _normalize_text(value)
    if not text:
        return text
    if text.startswith("base64:"):
        encoded = text.split(":", 1)[1].strip()
        try:
            return base64.b64decode(encoded, validate=True).decode("utf-8")
        except Exception:
            return text
    return text


def normalize_secret_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in payload.items():
        if value is None:
            continue
        if isinstance(value, Mapping):
            normalized[key] = normalize_secret_payload(value)
        elif isinstance(value, list):
            normalized[key] = [normalize_secret_payload(item) if isinstance(item, Mapping) else _normalize_text(item) for item in value]
        elif _is_secret_key(key):
            normalized[key] = _normalize_secret_value(value)
        else:
            normalized[key] = _normalize_text(value)
    return normalized


def _coerce_metadata(metadata: Any) -> dict[str, str]:
    if not metadata:
        return {}
    if not isinstance(metadata, Mapping):
        raise TypeError("metadata must be a mapping")
    return {str(k): _normalize_text(v) for k, v in metadata.items() if v is not None}


@dataclass(slots=True)
class SecretCreateRequest:
    name: str
    value: str
    metadata: dict[str, str] = field(default_factory=dict)
    version: str | None = None

    def __post_init__(self) -> None:
        self.name = _normalize_text(self.name)
        self.value = _normalize_secret_value(self.value)
        self.metadata = _coerce_metadata(self.metadata)
        self.version = _normalize_text(self.version) or None
        if not self.name:
            raise ValueError("name is required")
        if not self.value:
            raise ValueError("value is required")

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"name": self.name, "value": self.value}
        if self.metadata:
            data["metadata"] = dict(self.metadata)
        if self.version is not None:
            data["version"] = self.version
        return data


@dataclass(slots=True)
class SecretUpdateRequest:
    value: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)
    version: str | None = None

    def __post_init__(self) -> None:
        self.value = _normalize_secret_value(self.value) if self.value is not None else None
        self.metadata = _coerce_metadata(self.metadata)
        self.version = _normalize_text(self.version) or None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {}
        if self.value is not None:
            data["value"] = self.value
        if self.metadata:
            data["metadata"] = dict(self.metadata)
        if self.version is not None:
            data["version"] = self.version
        return data


@dataclass(slots=True)
class SecretResponse:
    name: str
    value: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)
    version: str | None = None
    created_at: str | None = None
    updated_at: str | None = None

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "SecretResponse":
        if not isinstance(payload, Mapping):
            raise TypeError("payload must be a mapping")
        name = _normalize_text(payload.get("name"))
        if not name:
            raise ValueError("name is required")
        metadata = _coerce_metadata(payload.get("metadata"))
        return cls(
            name=name,
            value=_normalize_secret_value(payload.get("value")) if payload.get("value") is not None else None,
            metadata=metadata,
            version=_normalize_text(payload.get("version")) or None,
            created_at=_normalize_text(payload.get("created_at")) or None,
            updated_at=_normalize_text(payload.get("updated_at")) or None,
        )

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"name": self.name}
        if self.value is not None:
            data["value"] = self.value
        if self.metadata:
            data["metadata"] = dict(self.metadata)
        if self.version is not None:
            data["version"] = self.version
        if self.created_at is not None:
            data["created_at"] = self.created_at
        if self.updated_at is not None:
            data["updated_at"] = self.updated_at
        return data


def load_secret_request(data: str | bytes | Mapping[str, Any]) -> SecretCreateRequest:
    if isinstance(data, Mapping):
        payload = dict(data)
    else:
        text = data.decode("utf-8") if isinstance(data, bytes) else data
        payload = json.loads(text)
    return SecretCreateRequest(
        name=payload.get("name", ""),
        value=payload.get("value", ""),
        metadata=payload.get("metadata", {}),
        version=payload.get("version"),
    )


def load_secret_response(data: str | bytes | Mapping[str, Any]) -> SecretResponse:
    if isinstance(data, Mapping):
        payload = dict(data)
    else:
        text = data.decode("utf-8") if isinstance(data, bytes) else data
        payload = json.loads(text)
    return SecretResponse.from_dict(payload)


def normalize_secret_env(prefix: str = "SECRET_") -> dict[str, str]:
    normalized: dict[str, str] = {}
    for key, value in os.environ.items():
        if key.startswith(prefix):
            normalized[key[len(prefix):].lower()] = _normalize_secret_value(value)
    return normalized

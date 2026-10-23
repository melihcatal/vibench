from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping
import base64
import hashlib
import json
import re


_SECRET_KEYS = {
    "secret",
    "password",
    "passwd",
    "token",
    "apikey",
    "api_key",
    "access_key",
    "private_key",
    "client_secret",
    "credential",
}

_SENSITIVE_PATTERNS = [
    re.compile(r"(^|[_\-])(secret|password|passwd|token|key|credential)s?($|[_\-])", re.IGNORECASE),
    re.compile(r"bearer\s+[a-z0-9._\-+/=]+", re.IGNORECASE),
    re.compile(r"(?i)-----BEGIN [A-Z ]+PRIVATE KEY-----"),
]


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str)


def _looks_sensitive_name(name: str) -> bool:
    n = name.lower()
    return any(key in n for key in _SECRET_KEYS) or any(pattern.search(n) for pattern in _SENSITIVE_PATTERNS)


def _mask_scalar(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, bytes):
        return "[REDACTED-BYTES]"
    if isinstance(value, str):
        if not value:
            return value
        if any(pattern.search(value) for pattern in _SENSITIVE_PATTERNS):
            return "[REDACTED]"
        if len(value) > 64:
            return f"[REDACTED:{hashlib.sha256(value.encode('utf-8')).hexdigest()[:12]}]"
        return value
    return "[REDACTED]"


def normalize_secret_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): normalize_secret_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [normalize_secret_value(v) for v in value]
    return _mask_scalar(value)


def normalize_secret_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in payload.items():
        key_str = str(key)
        normalized[key_str] = "[REDACTED]" if _looks_sensitive_name(key_str) else normalize_secret_value(value)
    return normalized


def build_secret_request(name: str, value: Any, metadata: Mapping[str, Any] | None = None) -> dict[str, Any]:
    request = {
        "name": name,
        "value": value,
        "metadata": dict(metadata or {}),
        "created_at": _now_utc().isoformat(),
    }
    request["value_fingerprint"] = hashlib.sha256(_stable_json(normalize_secret_value(value)).encode("utf-8")).hexdigest()
    return request


def build_secret_response(name: str, secret_id: str, status: str = "stored", metadata: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return {
        "name": name,
        "secret_id": secret_id,
        "status": status,
        "metadata": dict(metadata or {}),
        "timestamp": _now_utc().isoformat(),
    }


@dataclass(frozen=True)
class SecretRequest:
    name: str
    value: Any
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: _now_utc().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return build_secret_request(self.name, self.value, self.metadata)

    def normalized(self) -> dict[str, Any]:
        return normalize_secret_payload(self.to_dict())


@dataclass(frozen=True)
class SecretResponse:
    name: str
    secret_id: str
    status: str = "stored"
    metadata: dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: _now_utc().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return build_secret_response(self.name, self.secret_id, self.status, self.metadata)

    def normalized(self) -> dict[str, Any]:
        return normalize_secret_payload(self.to_dict())


def redact_secrets(obj: Any) -> Any:
    if isinstance(obj, Mapping):
        return {str(k): ("[REDACTED]" if _looks_sensitive_name(str(k)) else redact_secrets(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact_secrets(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(redact_secrets(v) for v in obj)
    if isinstance(obj, set):
        return {redact_secrets(v) for v in obj}
    return _mask_scalar(obj)


def secret_digest(value: Any) -> str:
    normalized = _stable_json(normalize_secret_value(value)).encode("utf-8")
    return base64.urlsafe_b64encode(hashlib.sha256(normalized).digest()).decode("ascii").rstrip("=")

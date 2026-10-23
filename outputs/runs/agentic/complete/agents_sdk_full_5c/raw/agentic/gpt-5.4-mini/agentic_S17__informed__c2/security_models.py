from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Mapping, Optional
import base64
import json


@dataclass
class CryptoRequest:
    key_name: str
    plaintext: Optional[str] = None
    ciphertext: Optional[str] = None
    signing_message: Optional[str] = None
    aad: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CryptoResponse:
    key_name: str
    operation: str
    payload: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedEvent:
    key_id: str
    action: str
    actor: str
    timestamp: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


def _to_str(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8")
        except Exception:
            return base64.b64encode(value).decode("ascii")
    return str(value)


def normalize_text_payload(value: Any) -> str:
    text = _to_str(value).strip()
    if text.startswith('"') and text.endswith('"'):
        try:
            parsed = json.loads(text)
            if isinstance(parsed, str):
                return parsed
        except Exception:
            pass
    return text


def normalize_event(raw: Mapping[str, Any]) -> NormalizedEvent:
    key_id = _to_str(raw.get("key_id") or raw.get("keyName") or raw.get("key") or raw.get("name"))
    action = _to_str(raw.get("action") or raw.get("operation") or raw.get("event") or raw.get("type"))
    actor = _to_str(raw.get("actor") or raw.get("principal") or raw.get("user") or raw.get("identity"))
    timestamp = raw.get("timestamp") or raw.get("time") or raw.get("created_at")
    details = {k: v for k, v in raw.items() if k not in {"key_id", "keyName", "key", "name", "action", "operation", "event", "type", "actor", "principal", "user", "identity", "timestamp", "time", "created_at"}}
    return NormalizedEvent(key_id=key_id, action=action, actor=actor, timestamp=_to_str(timestamp) if timestamp else None, details=details)


def normalize_usage_items(items: Iterable[Mapping[str, Any]]) -> list[NormalizedEvent]:
    return [normalize_event(item) for item in items]

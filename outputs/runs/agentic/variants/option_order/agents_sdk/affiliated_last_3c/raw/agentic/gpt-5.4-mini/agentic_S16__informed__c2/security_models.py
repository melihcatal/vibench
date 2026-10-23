from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, MutableMapping, Optional
import json


@dataclass(frozen=True)
class SecretRequest:
    secret_id: str
    version: Optional[str] = None
    stage: Optional[str] = None
    json_path: Optional[str] = None


@dataclass(frozen=True)
class SecretResponse:
    secret_id: str
    version: Optional[str]
    value: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class NormalizedText:
    raw: str
    compact: str
    lower: str


def normalize_secret_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def normalize_text(value: Any) -> NormalizedText:
    raw = normalize_secret_value(value)
    compact = " ".join(raw.split())
    return NormalizedText(raw=raw, compact=compact, lower=compact.lower())


def parse_json_maybe(value: Any) -> Dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    text = normalize_secret_value(value).strip()
    if not text:
        return {}
    return json.loads(text)

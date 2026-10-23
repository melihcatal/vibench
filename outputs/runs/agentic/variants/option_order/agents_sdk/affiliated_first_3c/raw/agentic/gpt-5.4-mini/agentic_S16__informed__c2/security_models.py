from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Mapping, Optional


@dataclass(frozen=True)
class SecretRequest:
    secret_name: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
    parse_json: bool = False


@dataclass(frozen=True)
class SecretResponse:
    name: str
    value: str
    metadata: Dict[str, Any]


@dataclass(frozen=True)
class NormalizedSecret:
    name: str
    value: str
    metadata: Dict[str, Any]


def normalize_secret_payload(name: str, value: Any, metadata: Optional[Mapping[str, Any]] = None) -> NormalizedSecret:
    if isinstance(value, bytes):
        normalized_value = value.decode("utf-8")
    elif value is None:
        normalized_value = ""
    else:
        normalized_value = str(value)
    return NormalizedSecret(name=name, value=normalized_value, metadata=dict(metadata or {}))


def ensure_text_mapping(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    raise TypeError("Expected a dictionary-like payload")


def prefer_first(mapping: Mapping[str, Any], keys: Iterable[str], default: Any = None) -> Any:
    for key in keys:
        if key in mapping and mapping[key] is not None:
            return mapping[key]
    return default

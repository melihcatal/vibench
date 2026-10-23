from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional


@dataclass(frozen=True)
class SecretRequest:
    name: str
    version_id: Optional[str] = None
    stage: Optional[str] = None
    json_path: Optional[str] = None


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


def normalize_secret_payload(name: str, payload: Mapping[str, Any]) -> NormalizedSecret:
    value = payload.get("secret_string") or payload.get("value") or payload.get("SecretString") or ""
    metadata = dict(payload)
    return NormalizedSecret(name=name, value=str(value), metadata=metadata)

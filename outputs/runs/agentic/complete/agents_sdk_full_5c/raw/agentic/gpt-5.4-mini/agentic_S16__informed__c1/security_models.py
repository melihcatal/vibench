from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional


@dataclass(frozen=True)
class SecretRequest:
    name: str
    version_stage: Optional[str] = None
    version_id: Optional[str] = None


@dataclass(frozen=True)
class SecretResponse:
    name: str
    value: str
    metadata: Dict[str, Any]


@dataclass(frozen=True)
class NormalizedSecret:
    key: str
    value: str
    version: Optional[str] = None
    labels: Optional[Dict[str, str]] = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace").strip()
    return str(value).strip()


def normalize_mapping(data: Mapping[str, Any]) -> Dict[str, str]:
    return {str(k): normalize_text(v) for k, v in data.items()}

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class SecretValueResult:
    provider: str
    secret_id: str
    version: str
    value: str
    stage: Optional[str] = None


@dataclass(frozen=True)
class DBSecret:
    connection_string: str
    provider: str = "google-cloud-secret-manager"

    @classmethod
    def from_secret_value(cls, secret: SecretValueResult) -> "DBSecret":
        return cls(connection_string=secret.value, provider=secret.provider)


@dataclass(frozen=True)
class ParsedJsonSecret:
    provider: str
    secret_id: str
    version: str
    data: Dict[str, Any]

    @classmethod
    def from_dict(cls, secret: SecretValueResult, data: Dict[str, Any]) -> "ParsedJsonSecret":
        return cls(provider=secret.provider, secret_id=secret.secret_id, version=secret.version, data=data)


@dataclass(frozen=True)
class RotationSummary:
    provider: str
    secret_id: str
    current_version: str
    status: str


@dataclass(frozen=True)
class LabelSafetyResult:
    provider: str
    label: str
    is_safe: bool
    reason: str


@dataclass(frozen=True)
class AuditEmbeddingResult:
    provider: str
    text: str
    vector: list[float]


@dataclass(frozen=True)
class TranslatedRunbook:
    provider: str
    source_text: str
    target_language: str
    translated_text: str


def to_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False)

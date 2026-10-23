from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Mapping, Optional


@dataclass(frozen=True)
class SecretRequest:
    name: str
    version: Optional[str] = None
    version_stage: Optional[str] = None


@dataclass(frozen=True)
class SecretResponse:
    name: str
    value: str
    version: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class NormalizedSecret:
    name: str
    raw_value: str
    parsed: Any


@dataclass(frozen=True)
class RotationSummaryResult:
    secret_name: str
    current_version: Optional[str]
    staged_versions: Iterable[str]
    status: str


@dataclass(frozen=True)
class SafetyCheckResult:
    label: str
    safe: bool
    reasons: Iterable[str]


@dataclass(frozen=True)
class EmbeddingResult:
    text: str
    vector: list[float]
    model: str


@dataclass(frozen=True)
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str]
    target_language: str


def normalize_secret_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, str):
        return value
    return str(value)


def extract_json_payload(value: Any) -> Any:
    import json

    text = normalize_secret_value(value).strip()
    if not text:
        return {}
    return json.loads(text)


def normalize_label_text(text: str) -> str:
    return " ".join(normalize_secret_value(text).split())

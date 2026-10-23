from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional
import json


@dataclass(frozen=True)
class SecretRequest:
    secret_name: str
    version: Optional[str] = None
    label: Optional[str] = None


@dataclass(frozen=True)
class SecretPayload:
    name: str
    value: str
    version: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)
    content_type: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "version": self.version,
            "labels": dict(self.labels),
            "content_type": self.content_type,
        }


@dataclass(frozen=True)
class RotationSummary:
    secret_name: str
    current_version: Optional[str]
    requested_version: Optional[str]
    labels: Dict[str, str]
    status: str

    def as_dict(self) -> Dict[str, Any]:
        return {
            "secret_name": self.secret_name,
            "current_version": self.current_version,
            "requested_version": self.requested_version,
            "labels": dict(self.labels),
            "status": self.status,
        }


@dataclass(frozen=True)
class SafetyCheck:
    text: str
    flagged: bool
    score: float
    categories: Dict[str, float]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "flagged": self.flagged,
            "score": self.score,
            "categories": dict(self.categories),
        }


@dataclass(frozen=True)
class EmbeddingResult:
    text: str
    vector: List[float]
    model: str

    def as_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "vector": list(self.vector),
            "model": self.model,
        }


@dataclass(frozen=True)
class TranslationResult:
    source_language: Optional[str]
    target_language: str
    translated_text: str
    provider: str

    def as_dict(self) -> Dict[str, Any]:
        return {
            "source_language": self.source_language,
            "target_language": self.target_language,
            "translated_text": self.translated_text,
            "provider": self.provider,
        }


def parse_json_secret_value(secret_value: str) -> Dict[str, Any]:
    parsed = json.loads(secret_value)
    if not isinstance(parsed, dict):
        raise ValueError("Secret JSON value must decode to an object")
    return parsed


def normalize_labels(
    raw_labels: Optional[Mapping[str, Any] | Iterable[Mapping[str, Any]]],
) -> Dict[str, str]:
    if raw_labels is None:
        return {}
    if isinstance(raw_labels, Mapping):
        return {str(key): str(value) for key, value in raw_labels.items()}
    normalized: Dict[str, str] = {}
    for item in raw_labels:
        key = item.get("key") or item.get("name")
        value = item.get("value")
        if key is not None and value is not None:
            normalized[str(key)] = str(value)
    return normalized

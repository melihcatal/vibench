from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass(frozen=True)
class SecretRequest:
    secret_id: str
    version_stage: Optional[str] = None
    version_id: Optional[str] = None


@dataclass(frozen=True)
class SecretResponse:
    secret_id: str
    payload: str
    version_id: Optional[str] = None
    version_stages: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class RotationSummary:
    secret_id: str
    current_version: Optional[str]
    previous_version: Optional[str]
    labels: List[str]


@dataclass(frozen=True)
class SafetyCheckResult:
    label: str
    note: str
    unsafe: bool
    reasons: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class EmbeddingDocument:
    document_id: str
    text: str
    embedding: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    target_language: str


@dataclass(frozen=True)
class TranslationResponse:
    text: str
    target_language: str
    translated_text: str


def normalize_mapping(data: Mapping[str, Any]) -> Dict[str, Any]:
    return {str(key): value for key, value in data.items()}


def normalize_iterable(values: Iterable[Any]) -> List[str]:
    return [str(value) for value in values]

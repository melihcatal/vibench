from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass(frozen=True)
class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str


@dataclass(frozen=True)
class MarkupTranslationRequest:
    markup: str
    source_language: str
    target_language: str
    format_type: str = "html"


@dataclass(frozen=True)
class DictionaryTranslationRequest:
    values: Dict[str, str]
    source_language: str
    target_language: str


@dataclass(frozen=True)
class TranslationResponse:
    translated_text: str
    provider: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BatchTranslationResponse:
    translated_texts: List[str]
    provider: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DictionaryTranslationResponse:
    translated_values: Dict[str, str]
    provider: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class QualityIssue:
    category: str
    severity: str
    detail: str
    score: float


@dataclass(frozen=True)
class QualitySummary:
    provider: str
    issues: List[QualityIssue]
    overall_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SafetyCheckResult:
    provider: str
    is_safe: bool
    labels: Dict[str, float]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EmbeddingResult:
    provider: str
    vectors: List[List[float]]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AudioPreviewResult:
    provider: str
    audio_content: bytes
    audio_format: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def preserve_order_mapping(keys: Iterable[str], translated_values: Iterable[str]) -> Dict[str, str]:
    return dict(zip(keys, translated_values))


def ensure_string_mapping(values: Mapping[str, Any]) -> Dict[str, str]:
    return {str(k): "" if v is None else str(v) for k, v in values.items()}

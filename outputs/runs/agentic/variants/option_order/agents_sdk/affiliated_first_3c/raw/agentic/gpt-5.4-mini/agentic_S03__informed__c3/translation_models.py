from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Sequence


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    source_language: str
    target_language: str
    preserve_tags: bool = False
    format_type: str = "text"


@dataclass(frozen=True)
class BatchTranslationRequest:
    texts: Sequence[str]
    source_language: str
    target_language: str
    preserve_tags: bool = False


@dataclass(frozen=True)
class TranslationResponse:
    translated_text: str
    provider: str
    source_language: str
    target_language: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BatchTranslationResponse:
    translated_texts: List[str]
    provider: str
    source_language: str
    target_language: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class QualitySummary:
    provider: str
    overall_score: float
    issues: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class UnsafeContentCheckResult:
    provider: str
    is_safe: bool
    labels: Dict[str, float]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TranslationMemoryEmbedding:
    provider: str
    vector: List[float]
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AudioPreview:
    provider: str
    audio_bytes: bytes
    voice: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_texts(values: Iterable[Any]) -> List[str]:
    return [normalize_text(v) for v in values]


def ensure_mapping(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return dict(value)
    raise TypeError("Expected a mapping-like value")

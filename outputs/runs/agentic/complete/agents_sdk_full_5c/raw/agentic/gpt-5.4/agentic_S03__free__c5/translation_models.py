from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable


@dataclass(slots=True)
class TranslationRequest:
    text: str
    source_language: str | None = None
    target_language: str = "en"
    content_type: str = "text/plain"


@dataclass(slots=True)
class BatchTranslationRequest:
    texts: list[str]
    source_language: str | None = None
    target_language: str = "en"
    content_type: str = "text/plain"


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    detected_source_language: str | None = None
    provider: str = "google_translate"
    model: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class QualitySummaryResult:
    summary: str
    provider: str
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SafetyCheckResult:
    is_safe: bool
    categories: list[str]
    rationale: str
    provider: str
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EmbeddingResult:
    vector: list[float]
    dimensions: int
    provider: str
    model: str
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AudioPreviewResult:
    audio_bytes: bytes
    content_type: str
    provider: str
    voice: str


def ensure_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def normalize_texts(values: Iterable[Any]) -> list[str]:
    return [ensure_text(v) for v in values]


def coerce_dictionary_values(data: dict[str, Any]) -> dict[str, str]:
    return {str(k): ensure_text(v) for k, v in data.items()}

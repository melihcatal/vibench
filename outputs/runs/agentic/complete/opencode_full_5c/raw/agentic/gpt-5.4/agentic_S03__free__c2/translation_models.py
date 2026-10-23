from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class TranslationRequest:
    text: str
    source_language: str
    target_language: str
    content_type: str = "text/plain"


@dataclass(slots=True)
class BatchTranslationRequest:
    texts: list[str]
    source_language: str
    target_language: str
    content_type: str = "text/plain"


@dataclass(slots=True)
class TranslationResult:
    text: str
    provider: str
    source_language: str
    target_language: str
    detected_language: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class QualitySummaryResult:
    summary: str
    issues: list[str]
    provider: str
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SafetyCheckResult:
    safe: bool
    categories: list[str]
    rationale: str
    provider: str
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EmbeddingResult:
    vector: list[float]
    dimensions: int
    provider: str
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AudioPreviewResult:
    audio_base64: str
    provider: str
    voice: str
    audio_format: str
    raw: dict[str, Any] = field(default_factory=dict)


def normalize_language_code(language: str) -> str:
    return language.strip().replace("_", "-").lower()


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def ensure_text_list(values: list[Any]) -> list[str]:
    return [normalize_text(value) for value in values]


def normalize_dictionary_values(data: dict[str, Any]) -> dict[str, str]:
    return {str(key): normalize_text(value) for key, value in data.items()}

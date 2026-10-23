from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping


@dataclass(slots=True)
class TranslationRequest:
    text: str
    source_language: str | None
    target_language: str


@dataclass(slots=True)
class BatchTranslationRequest:
    texts: list[str]
    source_language: str | None
    target_language: str


@dataclass(slots=True)
class TranslationResult:
    text: str
    detected_source_language: str | None = None
    provider: str = "google_translate"
    model: str | None = None


@dataclass(slots=True)
class QualitySummary:
    summary: str
    issues: list[str]
    provider: str
    model: str


@dataclass(slots=True)
class SafetyCheckResult:
    is_safe: bool
    categories: list[str]
    provider: str
    model: str


@dataclass(slots=True)
class EmbeddingResult:
    vector: list[float]
    provider: str
    model: str


def ensure_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def normalize_texts(values: Iterable[Any]) -> list[str]:
    return [ensure_text(value) for value in values]


def normalize_mapping_values(data: Mapping[str, Any]) -> dict[str, str]:
    return {str(key): ensure_text(value) for key, value in data.items()}

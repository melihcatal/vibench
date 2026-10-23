from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    source_language: str
    target_language: str
    glossary: Mapping[str, str] | None = None
    formality: str | None = None


@dataclass(frozen=True)
class BatchTranslationRequest:
    texts: Sequence[str]
    source_language: str
    target_language: str


@dataclass(frozen=True)
class TranslationResponse:
    translated_text: str
    detected_source_language: str | None = None
    raw: Any = None


@dataclass(frozen=True)
class BatchTranslationResponse:
    translated_texts: list[str] = field(default_factory=list)
    raw: Any = None


@dataclass(frozen=True)
class TranslationQualityIssue:
    category: str
    message: str
    severity: str = "medium"


@dataclass(frozen=True)
class UnsafeCopyResult:
    safe: bool
    issues: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class TranslationMemoryEmbeddingResult:
    segment: str
    embedding: list[float]
    model: str


@dataclass(frozen=True)
class AudioPreviewResult:
    audio_bytes: bytes
    voice: str
    model: str


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    if isinstance(text, str):
        return text.strip()
    return str(text).strip()


def normalize_text_list(texts: Sequence[Any]) -> list[str]:
    return [normalize_text(text) for text in texts]

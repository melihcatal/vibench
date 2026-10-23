from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence


@dataclass(slots=True)
class TranslationRequest:
    text: str
    source_language: str
    target_language: str
    glossary: Optional[Mapping[str, str]] = None
    formality: Optional[str] = None


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str
    provider: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class BatchTranslationResult:
    translated_texts: List[str]
    source_language: str
    target_language: str
    provider: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class QualityIssue:
    category: str
    severity: str
    message: str
    source_text: Optional[str] = None
    translated_text: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class UnsafeContentResult:
    flagged: bool
    provider: str
    score: float
    labels: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EmbeddingResult:
    vector: List[float]
    provider: str
    model: str
    dimensions: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AudioPreviewResult:
    audio_bytes: bytes
    provider: str
    voice: str
    content_type: str = "audio/mpeg"
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_texts(texts: Iterable[str]) -> List[str]:
    return [normalize_text(text) for text in texts]


def preserve_mapping_keys(data: Mapping[str, str]) -> Dict[str, str]:
    return dict(data)


def markdown_safe_text(text: str) -> str:
    return normalize_text(text)

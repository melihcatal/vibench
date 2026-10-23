from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence


@dataclass(slots=True)
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: str = "en"
    mime_type: str = "text/plain"
    glossary_config: Optional[Dict[str, Any]] = None

    def to_google_parent(self, project_id: str, location: str) -> str:
        return f"projects/{project_id}/locations/{location}"


@dataclass(slots=True)
class BatchTranslationRequest:
    texts: Sequence[str]
    source_language: Optional[str] = None
    target_language: str = "en"
    mime_type: str = "text/plain"

    def normalized_texts(self) -> List[str]:
        return [str(text) for text in self.texts]


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    detected_language: Optional[str] = None
    provider: str = "google-cloud-translate"
    model: Optional[str] = None
    raw: Optional[Any] = None


@dataclass(slots=True)
class BatchTranslationResult:
    translations: List[TranslationResult] = field(default_factory=list)

    def translated_texts(self) -> List[str]:
        return [item.translated_text for item in self.translations]


@dataclass(slots=True)
class QualitySummaryResult:
    summary: str
    issues: List[str] = field(default_factory=list)
    provider: str = "openai"
    model: str = "gpt-4o-mini"
    raw: Optional[Any] = None


@dataclass(slots=True)
class SafetyCheckResult:
    flagged: bool
    scores: Dict[str, float] = field(default_factory=dict)
    provider: str = "perspectiveapi"
    raw: Optional[Any] = None


@dataclass(slots=True)
class EmbeddingResult:
    embedding: List[float]
    dimensions: int
    provider: str = "openai"
    model: str = "text-embedding-3-small"
    raw: Optional[Any] = None


@dataclass(slots=True)
class AudioPreviewResult:
    audio_bytes: bytes
    content_type: str
    provider: str = "elevenlabs"
    voice_id: Optional[str] = None
    raw: Optional[Any] = None


def normalize_language_code(language_code: Optional[str]) -> Optional[str]:
    if language_code is None:
        return None
    cleaned = language_code.strip().replace("_", "-")
    return cleaned or None


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    return str(text)


def normalize_mapping_values(data: Mapping[str, Any]) -> Dict[str, str]:
    return {str(key): normalize_text(value) for key, value in data.items()}


def chunk_iterable(values: Sequence[str], chunk_size: int) -> Iterable[List[str]]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    for index in range(0, len(values), chunk_size):
        yield list(values[index:index + chunk_size])

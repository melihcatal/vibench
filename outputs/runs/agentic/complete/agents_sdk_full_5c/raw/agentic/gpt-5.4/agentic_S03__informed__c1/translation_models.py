from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence


@dataclass(slots=True)
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: str = "en"
    preserve_formatting: bool = False


@dataclass(slots=True)
class BatchTranslationRequest:
    texts: Sequence[str]
    source_language: Optional[str] = None
    target_language: str = "en"
    preserve_formatting: bool = False


@dataclass(slots=True)
class TranslationResult:
    text: str
    detected_source_language: Optional[str] = None
    billed_characters: Optional[int] = None
    provider: str = "DeepL"
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class BatchTranslationResult:
    translations: List[TranslationResult]
    provider: str = "DeepL"


@dataclass(slots=True)
class QualitySummaryResult:
    summary: str
    issues: List[str]
    provider: str = "OpenAI"
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SafetyCheckResult:
    is_safe: bool
    categories: Dict[str, float]
    provider: str = "Perspective API"
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EmbeddingResult:
    embeddings: List[List[float]]
    model: str
    provider: str = "OpenAI"
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AudioPreviewResult:
    audio_bytes: bytes
    audio_format: str
    provider: str = "ElevenLabs"
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def normalize_text_list(values: Sequence[Any]) -> List[str]:
    return [normalize_text(value) for value in values]


def normalize_string_mapping(values: Mapping[str, Any]) -> Dict[str, str]:
    return {str(key): normalize_text(value) for key, value in values.items()}

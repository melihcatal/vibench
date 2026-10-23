from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence


@dataclass(slots=True)
class TranslationRequest:
    text: str
    source_language: Optional[str]
    target_language: str
    text_type: str = "plain"
    glossary_id: Optional[str] = None


@dataclass(slots=True)
class BatchTranslationRequest:
    texts: Sequence[str]
    source_language: Optional[str]
    target_language: str
    text_type: str = "plain"
    glossary_id: Optional[str] = None


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    detected_source_language: Optional[str] = None
    provider: str = "deepl"
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class BatchTranslationResult:
    translations: List[TranslationResult]
    provider: str = "deepl"
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class QualitySummaryResult:
    summary: str
    issues: List[str]
    provider: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SafetyCheckResult:
    is_safe: bool
    categories: List[str]
    explanation: str
    provider: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EmbeddingResult:
    embedding: List[float]
    dimensions: int
    provider: str
    model: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AudioPreviewResult:
    audio_bytes: bytes
    content_type: str
    provider: str
    voice_id: str
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_language_code(code: Optional[str]) -> Optional[str]:
    if code is None:
        return None
    normalized = code.strip().replace("_", "-").upper()
    return normalized or None


def normalize_text_list(texts: Sequence[str]) -> List[str]:
    return [str(text) for text in texts]


def normalize_dictionary_values(data: Mapping[str, Any]) -> Dict[str, str]:
    return {str(key): str(value) for key, value in data.items()}

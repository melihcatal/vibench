from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranslationRequest:
    text: str
    source_language: Optional[str]
    target_language: str


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: Optional[str]
    target_language: str


@dataclass
class TranslationResult:
    text: str
    detected_source_language: Optional[str]
    provider: str
    model: Optional[str] = None
    raw_response: Optional[Any] = None


@dataclass
class QualitySummaryResult:
    summary: str
    issues: List[str]
    provider: str
    model: str
    raw_response: Optional[Any] = None


@dataclass
class SafetyCheckResult:
    is_safe: bool
    flagged_categories: List[str]
    scores: Dict[str, float]
    provider: str
    raw_response: Optional[Any] = None


@dataclass
class EmbeddingResult:
    embedding: List[float]
    dimensions: int
    provider: str
    model: str
    raw_response: Optional[Any] = None


@dataclass
class AudioPreviewResult:
    audio_bytes: bytes
    content_type: str
    provider: str
    voice: str
    raw_response: Optional[Any] = None


def compact_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def normalize_language_code(language: Optional[str]) -> Optional[str]:
    if language is None:
        return None
    cleaned = language.strip().replace("_", "-")
    return cleaned.lower() or None


def ensure_string_dict(values: Dict[str, Any]) -> Dict[str, str]:
    return {
        str(key): "" if value is None else str(value) for key, value in values.items()
    }

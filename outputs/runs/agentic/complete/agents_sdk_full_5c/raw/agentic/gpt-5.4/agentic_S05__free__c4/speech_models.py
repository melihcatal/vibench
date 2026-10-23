from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Optional


@dataclass(slots=True)
class StreamingTranscriptEvent:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    language_code: Optional[str] = None
    start_offset: Optional[float] = None
    end_offset: Optional[float] = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class StreamingConfig:
    sample_rate_hz: int = 16000
    encoding: str = "LINEAR16"
    language_code: str = "en-US"
    interim_results: bool = True
    punctuate: bool = True


@dataclass(slots=True)
class CaptionChunk:
    text: str
    speaker: Optional[str] = None
    timestamp: Optional[float] = None


@dataclass(slots=True)
class SafetyResult:
    flagged: bool
    categories: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SummaryResult:
    summary: str
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EmbeddingResult:
    vector: list[float]
    model: str
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    target_language: str
    raw: dict[str, Any] = field(default_factory=dict)


def normalize_whitespace(text: str) -> str:
    return " ".join((text or "").split())


def merge_caption_chunks(chunks: Iterable[CaptionChunk]) -> str:
    return normalize_whitespace(" ".join(chunk.text for chunk in chunks if chunk.text))

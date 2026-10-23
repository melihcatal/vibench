from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Optional


@dataclass(slots=True)
class TranscriptSegment:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    language: Optional[str] = None
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    words: List[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class StreamingConfig:
    language_code: str = "en-US"
    sample_rate_hz: int = 16000
    encoding: str = "LINEAR16"
    interim_results: bool = True
    punctuation: bool = True
    channels: int = 1
    model: str = "latest_long"


@dataclass(slots=True)
class StreamChunk:
    audio: bytes
    sequence: Optional[int] = None
    timestamp_ms: Optional[int] = None


@dataclass(slots=True)
class SafetyAssessment:
    is_safe: bool
    scores: dict[str, float] = field(default_factory=dict)
    flagged_categories: List[str] = field(default_factory=list)


@dataclass(slots=True)
class EmbeddingVector:
    text: str
    vector: List[float]
    model: str


@dataclass(slots=True)
class SummaryResult:
    summary: str
    model: str


@dataclass(slots=True)
class TranslationResult:
    source_text: str
    translated_text: str
    target_language: str



def normalize_transcript_text(text: str) -> str:
    return " ".join(text.strip().split())



def merge_segments(segments: Iterable[TranscriptSegment]) -> str:
    return " ".join(normalize_transcript_text(segment.text) for segment in segments if segment.text).strip()

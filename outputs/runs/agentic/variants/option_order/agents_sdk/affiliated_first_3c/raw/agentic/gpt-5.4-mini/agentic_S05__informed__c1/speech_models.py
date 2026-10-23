from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass(slots=True)
class StreamingSpeechConfig:
    language_code: str = "en-US"
    enable_punctuation: bool = True
    interim_results: bool = True
    sample_rate_hz: int = 16000
    encoding: str = "LINEAR16"


@dataclass(slots=True)
class TranscriptSegment:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    start_time_ms: Optional[int] = None
    end_time_ms: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SafetyVerdict:
    text: str
    unsafe: bool
    categories: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class MeetingSummary:
    summary: str
    bullets: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CaptionEmbedding:
    text: str
    vector: List[float]
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_transcript_text(text: str) -> str:
    return " ".join(text.split()).strip()


def merge_segments(segments: Iterable[TranscriptSegment]) -> str:
    return " ".join(normalize_transcript_text(seg.text) for seg in segments if seg.text).strip()

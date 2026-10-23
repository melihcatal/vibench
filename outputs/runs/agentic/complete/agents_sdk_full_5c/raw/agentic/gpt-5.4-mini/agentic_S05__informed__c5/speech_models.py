from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class TranscriptSegment:
    text: str
    is_final: bool = False
    language: Optional[str] = None
    confidence: Optional[float] = None
    start_time_ms: Optional[int] = None
    end_time_ms: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StreamingRecognitionConfig:
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    model: str = "chirp"
    interim_results: bool = True
    single_utterance: bool = False


@dataclass
class AudioChunk:
    data: bytes
    sample_rate_hz: int = 16000
    channels: int = 1


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyResult:
    text: str
    flagged: bool
    categories: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SummaryResult:
    transcript: str
    summary: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    text: str
    vector: List[float]
    dimensions: int
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def merge_segments(segments: Iterable[TranscriptSegment]) -> str:
    parts = [normalize_text(segment.text) for segment in segments if normalize_text(segment.text)]
    return " ".join(parts)


def as_dict(mapping: Mapping[str, Any]) -> Dict[str, Any]:
    return dict(mapping)

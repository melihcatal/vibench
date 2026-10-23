from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass(slots=True)
class StreamingSpeechConfig:
    language_code: str = "en-US"
    enable_punctuation: bool = True
    interim_results: bool = True
    sample_rate_hz: int = 16000
    channels: int = 1
    model: Optional[str] = None


@dataclass(slots=True)
class AudioChunk:
    data: bytes
    timestamp_ms: Optional[int] = None


@dataclass(slots=True)
class TranscriptSegment:
    text: str
    is_final: bool = False
    stability: Optional[float] = None
    language_code: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RecognitionEvent:
    segments: List[TranscriptSegment] = field(default_factory=list)
    audio_ms: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class NormalizedTranscript:
    text: str
    final: bool
    language_code: Optional[str] = None
    confidence: Optional[float] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CaptionChunk:
    text: str
    seq: int = 0
    final: bool = False


@dataclass(slots=True)
class SafetyResult:
    label: str
    score: float
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SummaryResult:
    text: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EmbeddingResult:
    vector: List[float]
    dimension: int
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def chunk_text(chunks: Iterable[CaptionChunk]) -> str:
    return " ".join(normalize_text(chunk.text) for chunk in chunks if normalize_text(chunk.text))

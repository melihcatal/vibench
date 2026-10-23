from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Optional


@dataclass(slots=True)
class TranscriptChunk:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    language_code: Optional[str] = None
    start_offset_ms: Optional[int] = None
    end_offset_ms: Optional[int] = None
    raw: Any = None


@dataclass(slots=True)
class StreamingOptions:
    sample_rate_hz: int = 16000
    encoding: str = "linear16"
    language_code: str = "en-US"
    interim_results: bool = True
    punctuate: bool = True
    model: str = "nova-2"
    channels: int = 1
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class SafetyResult:
    unsafe: bool
    flagged_categories: List[str] = field(default_factory=list)
    scores: dict[str, float] = field(default_factory=dict)
    raw: Any = None


@dataclass(slots=True)
class SummaryResult:
    summary: str
    raw: Any = None


@dataclass(slots=True)
class EmbeddingResult:
    vector: List[float]
    model: str
    raw: Any = None


def normalize_text(text: str) -> str:
    return " ".join(text.replace("\n", " ").split()).strip()


def merge_transcript_chunks(chunks: Iterable[TranscriptChunk]) -> str:
    parts = [normalize_text(chunk.text) for chunk in chunks if normalize_text(chunk.text)]
    return " ".join(parts).strip()


def to_transcript_chunk(text: str, *, is_final: bool = False, confidence: Optional[float] = None, raw: Any = None) -> TranscriptChunk:
    return TranscriptChunk(
        text=normalize_text(text),
        is_final=is_final,
        confidence=confidence,
        raw=raw,
    )

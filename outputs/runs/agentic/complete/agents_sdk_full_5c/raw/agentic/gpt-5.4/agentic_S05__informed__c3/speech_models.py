from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Optional


@dataclass(slots=True)
class StreamingConfig:
    sample_rate_hz: int = 16000
    encoding: str = "LINEAR16"
    language_code: str = "en-US"
    interim_results: bool = True
    enable_automatic_punctuation: bool = True
    channels: int = 1


@dataclass(slots=True)
class TranscriptAlternative:
    transcript: str
    confidence: Optional[float] = None


@dataclass(slots=True)
class TranscriptEvent:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    raw: Any = None
    alternatives: list[TranscriptAlternative] = field(default_factory=list)


@dataclass(slots=True)
class CaptionChunk:
    text: str
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    speaker: Optional[str] = None


@dataclass(slots=True)
class SafetyResult:
    is_unsafe: bool
    scores: dict[str, float]
    raw: Any = None


@dataclass(slots=True)
class SummaryResult:
    summary: str
    raw: Any = None


@dataclass(slots=True)
class EmbeddingResult:
    embedding: list[float]
    model: str
    raw: Any = None


def pcm_bytes_from_chunks(chunks: Iterable[bytes]) -> Iterable[bytes]:
    for chunk in chunks:
        if not chunk:
            continue
        yield chunk


def normalize_transcript_text(text: str) -> str:
    return " ".join(text.strip().split())


def merge_caption_chunks(chunks: Iterable[CaptionChunk]) -> str:
    return "\n".join(normalize_transcript_text(chunk.text) for chunk in chunks if chunk.text.strip())

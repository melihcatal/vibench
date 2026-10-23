from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional


@dataclass
class StreamingAudioChunk:
    audio: bytes
    is_final: bool = False


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    language: Optional[str] = None
    raw: dict = field(default_factory=dict)


@dataclass
class CaptionChunk:
    text: str
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None


@dataclass
class NormalizedTranscript:
    text: str
    final: bool
    chunks: List[CaptionChunk] = field(default_factory=list)


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_transcript_event(event: TranscriptEvent) -> NormalizedTranscript:
    return NormalizedTranscript(text=normalize_text(event.text), final=event.is_final)


def join_caption_chunks(chunks: Iterable[CaptionChunk]) -> str:
    return normalize_text(" ".join(chunk.text for chunk in chunks if chunk.text))

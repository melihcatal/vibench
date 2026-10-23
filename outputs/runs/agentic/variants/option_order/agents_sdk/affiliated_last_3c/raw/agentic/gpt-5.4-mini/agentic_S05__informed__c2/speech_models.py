from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Optional


@dataclass
class TranscriptChunk:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    language: Optional[str] = None
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    raw: Any = None


@dataclass
class StreamConfig:
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    interim_results: bool = True
    sample_rate_hz: int = 16000
    encoding: str = "LINEAR16"
    model: str = "latest_long"


@dataclass
class StreamResult:
    chunks: List[TranscriptChunk] = field(default_factory=list)
    raw_events: List[Any] = field(default_factory=list)

    def add(self, chunk: TranscriptChunk) -> None:
        self.chunks.append(chunk)

    def latest_text(self) -> str:
        return self.chunks[-1].text if self.chunks else ""


def normalize_transcript_text(text: str) -> str:
    return " ".join(text.strip().split())


def chunks_to_text(chunks: Iterable[TranscriptChunk], final_only: bool = False) -> str:
    texts = [c.text for c in chunks if (c.is_final or not final_only)]
    return normalize_transcript_text(" ".join(texts))

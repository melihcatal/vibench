from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Optional


@dataclass(slots=True)
class StreamingOptions:
    language_code: str = "en-US"
    sample_rate_hz: int = 16000
    encoding: str = "linear16"
    interim_results: bool = True
    automatic_punctuation: bool = True
    channels: int = 1
    model: str = "latest_long"


@dataclass(slots=True)
class TranscriptChunk:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    language_code: Optional[str] = None
    start_time_ms: Optional[int] = None
    end_time_ms: Optional[int] = None
    raw: Any = None


@dataclass(slots=True)
class AudioChunk:
    data: bytes
    sample_rate_hz: int = 16000


@dataclass(slots=True)
class TranscriptAccumulator:
    interim_text: str = ""
    final_texts: list[str] = field(default_factory=list)

    def add(self, chunk: TranscriptChunk) -> None:
        if chunk.is_final:
            if chunk.text:
                self.final_texts.append(chunk.text)
            self.interim_text = ""
        else:
            self.interim_text = chunk.text

    def combined_text(self) -> str:
        pieces = [*self.final_texts]
        if self.interim_text:
            pieces.append(self.interim_text)
        return " ".join(piece.strip() for piece in pieces if piece and piece.strip())


def duration_to_ms(duration: Any) -> Optional[int]:
    if duration is None:
        return None
    seconds = getattr(duration, "seconds", None)
    nanos = getattr(duration, "nanos", None)
    if seconds is None and hasattr(duration, "total_seconds"):
        return int(duration.total_seconds() * 1000)
    if seconds is None:
        return None
    nanos = nanos or 0
    return int((seconds * 1000) + (nanos / 1_000_000))


def normalize_google_streaming_result(result: Any) -> Optional[TranscriptChunk]:
    alternatives = getattr(result, "alternatives", None) or []
    if not alternatives:
        return None
    top = alternatives[0]
    return TranscriptChunk(
        text=getattr(top, "transcript", "").strip(),
        is_final=bool(getattr(result, "is_final", False)),
        confidence=getattr(top, "confidence", None),
        language_code=getattr(result, "language_code", None),
        start_time_ms=duration_to_ms(getattr(result, "result_end_offset", None)),
        end_time_ms=duration_to_ms(getattr(result, "result_end_offset", None)),
        raw=result,
    )


def collect_normalized_results(response: Any) -> list[TranscriptChunk]:
    normalized: list[TranscriptChunk] = []
    for result in getattr(response, "results", []) or []:
        item = normalize_google_streaming_result(result)
        if item is not None:
            normalized.append(item)
    return normalized


def merge_transcripts(chunks: Iterable[TranscriptChunk]) -> str:
    parts = [
        chunk.text.strip() for chunk in chunks if chunk.text and chunk.text.strip()
    ]
    return " ".join(parts)

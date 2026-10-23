from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Optional


@dataclass(slots=True)
class StreamingAudioChunk:
    data: bytes
    sample_rate_hz: int = 16000
    encoding: str = "linear16"
    channels: int = 1


@dataclass(slots=True)
class TranscriptSegment:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    language_code: Optional[str] = None
    start_offset_ms: Optional[int] = None
    end_offset_ms: Optional[int] = None
    raw: Any = None


@dataclass(slots=True)
class TranscriptAccumulator:
    interim_text: str = ""
    final_texts: list[str] = field(default_factory=list)

    def apply(self, segment: TranscriptSegment) -> str:
        if segment.is_final:
            cleaned = normalize_transcript_text(segment.text)
            if cleaned:
                self.final_texts.append(cleaned)
            self.interim_text = ""
        else:
            self.interim_text = normalize_transcript_text(segment.text)
        return self.current_text()

    def current_text(self) -> str:
        parts = [*self.final_texts]
        if self.interim_text:
            parts.append(self.interim_text)
        return " ".join(p for p in parts if p).strip()


def normalize_transcript_text(text: str) -> str:
    return " ".join((text or "").strip().split())


def join_transcript_segments(segments: Iterable[TranscriptSegment]) -> str:
    return " ".join(
        normalize_transcript_text(segment.text)
        for segment in segments
        if normalize_transcript_text(segment.text)
    ).strip()

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Optional


DEFAULT_SAMPLE_RATE = 16000
DEFAULT_CHANNELS = 1
DEFAULT_CHUNK_MS = 100


@dataclass(slots=True)
class AudioChunk:
    data: bytes
    sample_rate_hz: int = DEFAULT_SAMPLE_RATE
    channels: int = DEFAULT_CHANNELS
    mime_type: str = "audio/pcm"

    @property
    def duration_ms(self) -> int:
        bytes_per_sample = 2 * max(self.channels, 1)
        if bytes_per_sample <= 0 or self.sample_rate_hz <= 0:
            return 0
        return int((len(self.data) / bytes_per_sample) / self.sample_rate_hz * 1000)


@dataclass(slots=True)
class TranscriptSegment:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    language_code: Optional[str] = None
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    raw: Any = None


@dataclass(slots=True)
class StreamTranscript:
    segments: List[TranscriptSegment] = field(default_factory=list)

    def append(self, segment: TranscriptSegment) -> None:
        self.segments.append(segment)

    @property
    def final_text(self) -> str:
        return " ".join(s.text for s in self.segments if s.is_final and s.text).strip()

    @property
    def latest_partial(self) -> str:
        partials = [s.text for s in self.segments if not s.is_final and s.text]
        return partials[-1] if partials else ""


def normalize_whitespace(text: str) -> str:
    return " ".join((text or "").split())


def merge_transcript_chunks(chunks: Iterable[str]) -> str:
    return normalize_whitespace(" ".join(chunk for chunk in chunks if chunk))


def pcm16_bytes_from_frame(frame: bytes) -> bytes:
    return frame or b""

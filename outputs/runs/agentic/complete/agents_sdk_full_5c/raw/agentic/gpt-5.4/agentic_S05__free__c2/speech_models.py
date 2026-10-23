from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Optional


@dataclass(slots=True)
class StreamingConfig:
    sample_rate_hz: int = 16000
    encoding: str = "linear16"
    language_code: str = "en-US"
    interim_results: bool = True
    punctuate: bool = True
    profanity_filter: bool = False
    model: str = "nova-2"


@dataclass(slots=True)
class AudioChunk:
    data: bytes
    sequence_id: Optional[int] = None
    ts_ms: Optional[int] = None


@dataclass(slots=True)
class TranscriptSegment:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    speaker: Optional[int] = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class PartialTranscriptState:
    interim_text: str = ""
    final_segments: List[TranscriptSegment] = field(default_factory=list)

    @property
    def full_text(self) -> str:
        parts = [seg.text.strip() for seg in self.final_segments if seg.text.strip()]
        if self.interim_text.strip():
            parts.append(self.interim_text.strip())
        return " ".join(parts).strip()


@dataclass(slots=True)
class CaptionChunk:
    text: str
    language: str = "en"
    speaker: Optional[str] = None
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None


def normalize_whitespace(text: str) -> str:
    return " ".join((text or "").split())


def merge_transcript_text(chunks: Iterable[str]) -> str:
    return normalize_whitespace(" ".join(chunk for chunk in chunks if chunk))


def deepgram_result_to_segment(result: dict[str, Any]) -> TranscriptSegment:
    channel = ((result.get("channel") or {}).get("alternatives") or [{}])[0]
    words = channel.get("words") or []
    text = normalize_whitespace(channel.get("transcript") or "")
    confidence = channel.get("confidence")
    start_ms = int(words[0]["start"] * 1000) if words else None
    end_ms = int(words[-1]["end"] * 1000) if words else None
    speaker = words[0].get("speaker") if words and "speaker" in words[0] else None
    return TranscriptSegment(
        text=text,
        is_final=bool(result.get("is_final")),
        confidence=confidence,
        start_ms=start_ms,
        end_ms=end_ms,
        speaker=speaker,
        raw=result,
    )

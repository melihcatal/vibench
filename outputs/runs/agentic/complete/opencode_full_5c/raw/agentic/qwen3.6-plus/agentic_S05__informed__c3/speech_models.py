from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class AudioChunk:
    pcm_bytes: bytes
    sample_rate: int = 16000
    channels: int = 1
    bit_depth: int = 16
    timestamp: float = field(default_factory=time.time)

    @property
    def duration_seconds(self) -> float:
        bytes_per_sample = self.bit_depth // 8
        samples = len(self.pcm_bytes) // (bytes_per_sample * self.channels)
        return samples / self.sample_rate


@dataclass
class TranscriptSegment:
    text: str
    start: float = 0.0
    end: float = 0.0
    confidence: float = 0.0


@dataclass
class TranscriptResult:
    is_final: bool
    text: str
    segments: list[TranscriptSegment] = field(default_factory=list)
    language: str = ""
    channel_index: int = 0
    timestamp: float = field(default_factory=time.time)

    @property
    def full_text(self) -> str:
        return (
            " ".join(seg.text for seg in self.segments) if self.segments else self.text
        )


@dataclass
class StreamingEvent:
    event_type: str
    result: TranscriptResult | None = None
    raw_payload: dict | None = None


def normalize_deepgram_result(payload: dict) -> TranscriptResult:
    channel = payload.get("channel", {})
    alternatives = channel.get("alternatives", [])
    if not alternatives:
        return TranscriptResult(
            is_final=payload.get("is_final", False),
            text="",
        )

    alt = alternatives[0]
    text = alt.get("transcript", "")
    words = alt.get("words", [])

    segments = [
        TranscriptSegment(
            text=w.get("word", ""),
            start=w.get("start", 0.0),
            end=w.get("end", 0.0),
            confidence=w.get("confidence", 0.0),
        )
        for w in words
    ]

    return TranscriptResult(
        is_final=payload.get("is_final", False),
        text=text,
        segments=segments,
        language=payload.get("channel", {}).get("language", ""),
        channel_index=payload.get("channel_index", 0),
    )


def merge_final_results(results: list[TranscriptResult]) -> str:
    final_texts = [r.text.strip() for r in results if r.is_final and r.text.strip()]
    return " ".join(final_texts)


def extract_interim_text(result: TranscriptResult) -> str:
    if not result.is_final:
        return result.text.strip()
    return ""

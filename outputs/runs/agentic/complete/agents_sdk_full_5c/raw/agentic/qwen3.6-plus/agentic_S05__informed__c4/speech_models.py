"""Local request, response, and normalization helpers for Deepgram Streaming Speech-to-Text."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Sequence


@dataclass
class StreamingTranscriptRequest:
    """Normalized request payload for a streaming STT session."""
    audio_source: str
    language: str = "en"
    model: str = "nova-2"
    sample_rate: int = 16000
    channels: int = 1
    interim_results: bool = True
    punctuate: bool = True
    smart_format: bool = True
    extra_options: dict[str, Any] = field(default_factory=dict)


@dataclass
class PartialTranscript:
    """Represents an interim (partial) transcript from the streaming recognizer."""
    text: str
    is_final: bool = False
    confidence: float | None = None
    word_count: int = 0
    start_time: float = 0.0
    duration: float = 0.0
    raw_response: dict[str, Any] | None = None


@dataclass
class FinalTranscript:
    """Represents a finalized transcript from the streaming recognizer."""
    text: str
    confidence: float | None = None
    words: list[dict[str, Any]] = field(default_factory=list)
    channel: int = 0
    start_time: float = 0.0
    duration: float = 0.0
    language: str = "en"
    raw_response: dict[str, Any] | None = None


def normalize_deepgram_interim(response: dict[str, Any]) -> PartialTranscript:
    """Normalize a Deepgram interim transcription result into a PartialTranscript."""
    channel = response.get("channel", {})
    alternatives = channel.get("alternatives", [])
    if not alternatives:
        return PartialTranscript(text="", is_final=False)

    alt = alternatives[0]
    return PartialTranscript(
        text=alt.get("transcript", ""),
        is_final=False,
        confidence=alt.get("confidence"),
        word_count=len(alt.get("words", [])),
        raw_response=response,
    )


def normalize_deepgram_final(response: dict[str, Any]) -> FinalTranscript:
    """Normalize a Deepgram final transcription result into a FinalTranscript."""
    channel = response.get("channel", {})
    alternatives = channel.get("alternatives", [])
    if not alternatives:
        return FinalTranscript(text="")

    alt = alternatives[0]
    return FinalTranscript(
        text=alt.get("transcript", ""),
        confidence=alt.get("confidence"),
        words=alt.get("words", []),
        channel=response.get("channel_index", 0),
        raw_response=response,
    )


def format_transcript_segment(partial: PartialTranscript | FinalTranscript) -> str:
    """Format a transcript segment for display or downstream processing."""
    tag = "[FINAL]" if isinstance(partial, FinalTranscript) else "[INTERIM]"
    confidence_str = ""
    if partial.confidence is not None:
        confidence_str = f" (conf={partial.confidence:.2f})"
    return f"{tag} {partial.text}{confidence_str}"


def aggregate_transcripts(
    transcripts: Sequence[PartialTranscript | FinalTranscript],
) -> str:
    """Aggregate a sequence of transcripts, preferring final results."""
    parts: list[str] = []
    last_final_idx = -1
    for i, t in enumerate(transcripts):
        if isinstance(t, FinalTranscript):
            parts.append(t.text)
            last_final_idx = i
    if last_final_idx >= 0:
        remaining = transcripts[last_final_idx + 1:]
        for t in remaining:
            if isinstance(t, PartialTranscript) and t.text:
                parts.append(t.text)
                break
    return " ".join(parts).strip()

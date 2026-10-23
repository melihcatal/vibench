from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Optional


@dataclass(slots=True)
class StreamingRecognitionConfig:
    sample_rate_hz: int = 16000
    language_code: str = "en-US"
    interim_results: bool = True
    enable_automatic_punctuation: bool = True
    encoding: str = "linear16"
    channels: int = 1


@dataclass(slots=True)
class TranscriptEvent:
    text: str
    is_final: bool = False
    stability: Optional[float] = None
    confidence: Optional[float] = None
    language_code: Optional[str] = None
    raw: Any = None


@dataclass(slots=True)
class CaptionChunk:
    text: str
    sequence_id: int
    started_at_ms: Optional[int] = None
    ended_at_ms: Optional[int] = None
    speaker: Optional[str] = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class NormalizedTranscript:
    text: str
    is_final: bool
    confidence: Optional[float]
    stability: Optional[float]
    provider: str


def normalize_transcript_text(text: str) -> str:
    return " ".join(text.replace("\n", " ").split()).strip()


def merge_caption_chunks(chunks: Iterable[CaptionChunk]) -> str:
    parts: List[str] = []
    for chunk in chunks:
        clean = normalize_transcript_text(chunk.text)
        if clean:
            parts.append(clean)
    return " ".join(parts)


def azure_result_to_event(result: Any, *, language_code: Optional[str] = None) -> TranscriptEvent:
    text = normalize_transcript_text(getattr(result, "text", ""))
    confidence = None
    if hasattr(result, "properties"):
        confidence = result.properties.get("SpeechServiceResponse_JsonResult")
    return TranscriptEvent(
        text=text,
        is_final=bool(text),
        stability=None,
        confidence=None,
        language_code=language_code,
        raw=result,
    )


def to_normalized_transcript(event: TranscriptEvent, *, provider: str) -> NormalizedTranscript:
    return NormalizedTranscript(
        text=normalize_transcript_text(event.text),
        is_final=event.is_final,
        confidence=event.confidence,
        stability=event.stability,
        provider=provider,
    )

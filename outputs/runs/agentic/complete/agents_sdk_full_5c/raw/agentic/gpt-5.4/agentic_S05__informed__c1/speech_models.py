from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass(slots=True)
class StreamingTranscriptChunk:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    language: Optional[str] = None
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class StreamingRecognitionConfig:
    language: str = "en-US"
    interim_results: bool = True
    punctuate: bool = True
    sample_rate_hz: int = 16000
    encoding: str = "linear16"
    model: str = "nova-2"


@dataclass(slots=True)
class CaptionSafetyResult:
    text: str
    unsafe: bool
    scores: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class MeetingSummaryResult:
    summary: str
    action_items: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class CaptionEmbeddingResult:
    text: str
    embedding: List[float]
    model: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TranslationResult:
    source_text: str
    translated_text: str
    target_language: str
    detected_source_language: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_transcript_text(text: str) -> str:
    return " ".join(text.strip().split())


def transcript_from_deepgram_result(result: Dict[str, Any]) -> List[StreamingTranscriptChunk]:
    channel = (result.get("channel") or {})
    alternatives = channel.get("alternatives") or []
    if not alternatives:
        return []
    alt = alternatives[0]
    text = normalize_transcript_text(alt.get("transcript", ""))
    if not text:
        return []
    confidence = alt.get("confidence")
    return [
        StreamingTranscriptChunk(
            text=text,
            is_final=bool(result.get("is_final", False)),
            confidence=confidence,
            language=result.get("metadata", {}).get("language"),
            raw=result,
        )
    ]


def join_caption_chunks(chunks: Iterable[str]) -> str:
    return normalize_transcript_text(" ".join(chunk for chunk in chunks if chunk))

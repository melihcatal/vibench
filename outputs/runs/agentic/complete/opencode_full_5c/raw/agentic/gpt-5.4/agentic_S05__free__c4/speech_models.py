from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Optional


@dataclass(slots=True)
class StreamingAudioChunk:
    content: bytes


@dataclass(slots=True)
class StreamingTranscriptEvent:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    language_code: Optional[str] = None
    raw: Any = None


@dataclass(slots=True)
class StreamingSessionConfig:
    sample_rate_hz: int = 16000
    encoding: str = "LINEAR16"
    language_code: str = "en-US"
    interim_results: bool = True
    enable_automatic_punctuation: bool = True


@dataclass(slots=True)
class CaptionSegment:
    text: str
    speaker: Optional[str] = None
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    metadata: dict[str, Any] = field(default_factory=dict)


def normalize_transcript_text(text: str) -> str:
    return " ".join(text.split())


def merge_caption_segments(segments: Iterable[CaptionSegment]) -> str:
    return " ".join(
        normalize_transcript_text(segment.text) for segment in segments if segment.text
    ).strip()


def transcript_events_from_google(response: Any) -> List[StreamingTranscriptEvent]:
    events: List[StreamingTranscriptEvent] = []
    for result in getattr(response, "results", []) or []:
        alternatives = getattr(result, "alternatives", []) or []
        if not alternatives:
            continue
        top = alternatives[0]
        events.append(
            StreamingTranscriptEvent(
                text=normalize_transcript_text(getattr(top, "transcript", "")),
                is_final=bool(getattr(result, "is_final", False)),
                confidence=getattr(top, "confidence", None),
                language_code=None,
                raw=result,
            )
        )
    return events

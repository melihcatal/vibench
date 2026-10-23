from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, AsyncIterable, AsyncIterator, Dict, Iterable, List, Optional


@dataclass
class StreamingAudioChunk:
    audio: bytes


@dataclass
class StreamingTranscriptAlternative:
    transcript: str
    confidence: Optional[float] = None


@dataclass
class StreamingTranscriptEvent:
    text: str
    is_final: bool
    stability: Optional[float] = None
    confidence: Optional[float] = None
    alternatives: List[StreamingTranscriptAlternative] = field(default_factory=list)
    raw: Optional[Any] = None


@dataclass
class StreamingRecognitionConfig:
    language_code: str = "en-US"
    sample_rate_hertz: int = 16000
    audio_encoding: str = "LINEAR16"
    enable_automatic_punctuation: bool = True
    interim_results: bool = True


async def normalize_async_audio_source(
    source: AsyncIterable[bytes],
) -> AsyncIterator[StreamingAudioChunk]:
    async for chunk in source:
        if chunk:
            yield StreamingAudioChunk(audio=chunk)


def normalize_google_streaming_response(
    response: Any,
) -> List[StreamingTranscriptEvent]:
    events: List[StreamingTranscriptEvent] = []
    for result in getattr(response, "results", []) or []:
        alternatives = [
            StreamingTranscriptAlternative(
                transcript=alt.transcript,
                confidence=getattr(alt, "confidence", None),
            )
            for alt in getattr(result, "alternatives", []) or []
        ]
        primary = (
            alternatives[0]
            if alternatives
            else StreamingTranscriptAlternative(transcript="")
        )
        events.append(
            StreamingTranscriptEvent(
                text=primary.transcript,
                is_final=bool(getattr(result, "is_final", False)),
                stability=getattr(result, "stability", None),
                confidence=primary.confidence,
                alternatives=alternatives,
                raw=result,
            )
        )
    return events


def merge_event_text(events: Iterable[StreamingTranscriptEvent]) -> str:
    return " ".join(
        event.text.strip() for event in events if event.text.strip()
    ).strip()


def provider_headers(provider: str) -> Dict[str, str]:
    return {"provider": provider, "content-type": "application/json"}

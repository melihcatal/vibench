from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, AsyncIterable, Dict, Iterable, List, Optional


@dataclass(slots=True)
class StreamingAudioChunk:
    content: bytes


@dataclass(slots=True)
class StreamingTranscriptEvent:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    language_code: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class StreamSettings:
    sample_rate_hz: int = 16000
    language_code: str = "en-US"
    interim_results: bool = True
    enable_automatic_punctuation: bool = True
    audio_encoding: str = "LINEAR16"


def normalize_bytes_chunk(chunk: bytes | bytearray | memoryview) -> StreamingAudioChunk:
    if isinstance(chunk, memoryview):
        data = chunk.tobytes()
    else:
        data = bytes(chunk)
    return StreamingAudioChunk(content=data)


def build_google_streaming_config(settings: StreamSettings) -> Dict[str, Any]:
    return {
        "config": {
            "encoding": settings.audio_encoding,
            "sample_rate_hertz": settings.sample_rate_hz,
            "language_code": settings.language_code,
            "enable_automatic_punctuation": settings.enable_automatic_punctuation,
        },
        "interim_results": settings.interim_results,
    }


def parse_google_streaming_response(response: Any) -> List[StreamingTranscriptEvent]:
    events: List[StreamingTranscriptEvent] = []
    for result in getattr(response, "results", []) or []:
        alternatives = getattr(result, "alternatives", []) or []
        if not alternatives:
            continue
        best = alternatives[0]
        events.append(
            StreamingTranscriptEvent(
                text=getattr(best, "transcript", ""),
                is_final=bool(getattr(result, "is_final", False)),
                confidence=getattr(best, "confidence", None),
                language_code=getattr(response, "language_code", None),
                raw={"result": result, "alternative": best},
            )
        )
    return events


async def iter_async_bytes(
    source: AsyncIterable[bytes],
) -> AsyncIterable[StreamingAudioChunk]:
    async for chunk in source:
        if chunk:
            yield normalize_bytes_chunk(chunk)


def merge_final_transcripts(events: Iterable[StreamingTranscriptEvent]) -> str:
    return " ".join(
        event.text.strip() for event in events if event.is_final and event.text.strip()
    )

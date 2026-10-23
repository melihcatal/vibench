from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class StreamingAudioChunk:
    data: bytes
    is_final: bool = False


@dataclass
class StreamingTranscriptEvent:
    text: str
    is_final: bool = False
    language: Optional[str] = None
    confidence: Optional[float] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CaptionChunk:
    text: str
    speaker: Optional[str] = None
    timestamp_ms: Optional[int] = None


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_chunks(
    chunks: Iterable[StreamingAudioChunk],
) -> List[StreamingAudioChunk]:
    return [
        StreamingAudioChunk(data=c.data, is_final=c.is_final) for c in chunks if c.data
    ]


def event_from_deepgram(payload: Dict[str, Any]) -> StreamingTranscriptEvent:
    alt = ((payload.get("channel") or {}).get("alternatives") or [{}])[0]
    text = normalize_text(alt.get("transcript", ""))
    return StreamingTranscriptEvent(
        text=text,
        is_final=bool(payload.get("is_final") or payload.get("speech_final")),
        language=payload.get("language"),
        confidence=alt.get("confidence"),
        raw=payload,
    )

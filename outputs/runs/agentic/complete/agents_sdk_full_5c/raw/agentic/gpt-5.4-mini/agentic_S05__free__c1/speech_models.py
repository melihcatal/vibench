from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class StreamingChunk:
    content: bytes
    timestamp_ms: Optional[int] = None


@dataclass
class TranscriptEvent:
    transcript: str
    is_final: bool
    stability: Optional[float] = None
    confidence: Optional[float] = None


def normalize_transcript(text: str) -> str:
    return " ".join(text.strip().split())


def chunk_to_request(chunk: StreamingChunk) -> Dict[str, Any]:
    return {"audio_content": chunk.content}


def parse_events(events: Iterable[Any]) -> List[TranscriptEvent]:
    normalized: List[TranscriptEvent] = []
    for e in events:
        normalized.append(
            TranscriptEvent(
                transcript=normalize_transcript(getattr(e, "transcript", "")),
                is_final=bool(getattr(e, "is_final", False)),
                stability=getattr(e, "stability", None),
                confidence=getattr(e, "confidence", None),
            )
        )
    return normalized

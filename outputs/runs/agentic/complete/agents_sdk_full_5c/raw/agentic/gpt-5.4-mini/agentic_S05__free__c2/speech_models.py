from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class TranscriptSegment:
    text: str
    is_final: bool = False
    stability: Optional[float] = None


@dataclass
class NormalizedStreamingEvent:
    transcript: str
    final: bool
    confidence: Optional[float] = None


def normalize_transcript(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_events(events: Iterable[Any]) -> List[NormalizedStreamingEvent]:
    normalized: List[NormalizedStreamingEvent] = []
    for event in events:
        transcript = normalize_transcript(getattr(event, "transcript", str(event)))
        final = bool(getattr(event, "is_final", getattr(event, "final", False)))
        confidence = getattr(event, "confidence", None)
        normalized.append(NormalizedStreamingEvent(transcript=transcript, final=final, confidence=confidence))
    return normalized


def event_to_dict(event: NormalizedStreamingEvent) -> Dict[str, Any]:
    return {"transcript": event.transcript, "final": event.final, "confidence": event.confidence}

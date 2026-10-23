from dataclasses import dataclass, field
from typing import Any, Iterable


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool = False
    confidence: float | None = None
    language: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class TranscriptChunk:
    audio: bytes
    timestamp_ms: int | None = None


def coerce_events(items: Iterable[dict[str, Any]]) -> list[TranscriptEvent]:
    events: list[TranscriptEvent] = []
    for item in items:
        events.append(
            TranscriptEvent(
                text=str(item.get("text", "")),
                is_final=bool(item.get("is_final", False)),
                confidence=item.get("confidence"),
                language=item.get("language"),
                raw=item,
            )
        )
    return events

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Optional


@dataclass
class AudioChunk:
    audio: bytes
    is_final: bool = False


@dataclass
class SpeechConfig:
    language_code: str = "en-US"
    enable_punctuation: bool = True


@dataclass
class TranscriptEvent:
    text: str
    is_partial: bool = False
    confidence: Optional[float] = None
    metadata: dict = field(default_factory=dict)


@dataclass
class TranscriptSegment:
    text: str
    is_final: bool = True
    confidence: Optional[float] = None


def normalize_transcript_events(events: Iterable[TranscriptEvent]) -> List[TranscriptEvent]:
    normalized: List[TranscriptEvent] = []
    for event in events:
        normalized.append(TranscriptEvent(text=(event.text or "").strip(), is_partial=bool(event.is_partial), confidence=event.confidence, metadata=dict(event.metadata)))
    return normalized

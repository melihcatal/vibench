from dataclasses import dataclass
from typing import Iterable, List, Optional


@dataclass
class SpeechChunk:
    audio: bytes
    timestamp_ms: Optional[int] = None


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool = False
    language: Optional[str] = None
    confidence: Optional[float] = None


@dataclass
class TranscriptionRequest:
    language_code: str = "en-US"
    enable_punctuation: bool = True
    interim_results: bool = True


def normalize_transcript(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_events(events: Iterable[TranscriptEvent]) -> List[TranscriptEvent]:
    return [
        TranscriptEvent(
            text=normalize_transcript(e.text),
            is_final=e.is_final,
            language=e.language,
            confidence=e.confidence,
        )
        for e in events
    ]

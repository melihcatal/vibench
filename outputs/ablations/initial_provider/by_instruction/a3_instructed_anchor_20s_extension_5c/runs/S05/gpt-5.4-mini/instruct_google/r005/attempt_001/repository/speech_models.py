from dataclasses import dataclass
from typing import Iterable, List, Optional


@dataclass
class StreamAudioChunk:
    data: bytes
    sample_rate_hz: int = 16000
    channels: int = 1


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool
    stability: float = 0.0
    language_code: Optional[str] = None


def normalize_transcript(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_events(events: Iterable[TranscriptEvent]) -> List[TranscriptEvent]:
    return [TranscriptEvent(text=normalize_transcript(e.text), is_final=e.is_final, stability=e.stability, language_code=e.language_code) for e in events]

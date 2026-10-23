from dataclasses import dataclass
from typing import Iterable, Iterator, Optional


@dataclass
class SpeechChunk:
    audio: bytes
    is_final: bool = False


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool
    language: Optional[str] = None


def normalize_transcript(text: str) -> str:
    return " ".join(text.strip().split())


def iter_transcript_text(events: Iterable[TranscriptEvent]) -> Iterator[str]:
    for event in events:
        text = normalize_transcript(event.text)
        if text:
            yield text

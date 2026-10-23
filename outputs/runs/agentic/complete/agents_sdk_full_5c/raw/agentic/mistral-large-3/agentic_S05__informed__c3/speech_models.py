from dataclasses import dataclass
from typing import Optional

@dataclass
class TranscriptEvent:
    text: str
    is_final: bool
    language: Optional[str] = None
    confidence: Optional[float] = None

def normalize_transcript(event: TranscriptEvent) -> str:
    return event.text.strip()
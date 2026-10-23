from dataclasses import dataclass
from typing import Optional

@dataclass
class TranscriptEvent:
    text: str
    is_final: bool
    timestamp: int

@dataclass
class NormalizedTranscript:
    text: str
    language: str
    confidence: float

def normalize_transcript(event: TranscriptEvent) -> NormalizedTranscript:
    return NormalizedTranscript(
        text=event.text.strip(),
        language="zh",
        confidence=1.0 if event.is_final else 0.8
    )
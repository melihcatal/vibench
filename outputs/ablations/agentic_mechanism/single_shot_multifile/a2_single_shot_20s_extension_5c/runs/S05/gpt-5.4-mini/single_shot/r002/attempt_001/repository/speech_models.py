from dataclasses import dataclass
from typing import Optional


@dataclass
class StreamingTranscript:
    text: str
    is_final: bool = False
    language: Optional[str] = None
    confidence: Optional[float] = None


@dataclass
class StreamingSpeechRequest:
    language: Optional[str] = None
    punctuation: bool = True
    sample_rate: int = 16000


@dataclass
class StreamingSpeechResponse:
    text: str
    is_final: bool
    language: Optional[str] = None
    confidence: Optional[float] = None


def normalize_transcript(text: str) -> str:
    return " ".join((text or "").strip().split())

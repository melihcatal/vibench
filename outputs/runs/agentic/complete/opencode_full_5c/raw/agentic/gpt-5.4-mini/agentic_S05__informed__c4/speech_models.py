from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_text(value: Optional[str]) -> str:
    return " ".join((value or "").split())


@dataclass
class AudioChunk:
    data: bytes
    is_final: bool = False


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool = False
    language: Optional[str] = None
    confidence: Optional[float] = None


@dataclass
class CaptionChunk:
    text: str
    timestamp_ms: Optional[int] = None


def event_to_dict(event: TranscriptEvent) -> Dict[str, Any]:
    return {
        "text": normalize_text(event.text),
        "is_final": event.is_final,
        "language": event.language,
        "confidence": event.confidence,
    }

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class StreamingSpeechConfig:
    language: str = "en-US"
    enable_punctuation: bool = True
    sample_rate_hz: int = 16000
    encoding: str = "pcm16"
    model: str = "default"


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    words: List[Dict[str, Any]] = field(default_factory=list)


def normalize_transcript_text(text: Optional[str]) -> str:
    return " ".join((text or "").strip().split())


def normalize_event(payload: Any) -> TranscriptEvent:
    if isinstance(payload, TranscriptEvent):
        return payload
    text = (
        getattr(payload, "text", None)
        or getattr(payload, "transcript", None)
        or getattr(payload, "alternatives", [{}])[0].get("transcript", "")
        if hasattr(payload, "alternatives")
        else ""
    )
    is_final = bool(
        getattr(payload, "is_final", False) or getattr(payload, "final", False)
    )
    confidence = getattr(payload, "confidence", None)
    words = getattr(payload, "words", []) or []
    return TranscriptEvent(
        text=normalize_transcript_text(text),
        is_final=is_final,
        confidence=confidence,
        words=words,
    )


def iter_normalized_text(events: Iterable[Any]) -> List[str]:
    return [normalize_event(event).text for event in events]

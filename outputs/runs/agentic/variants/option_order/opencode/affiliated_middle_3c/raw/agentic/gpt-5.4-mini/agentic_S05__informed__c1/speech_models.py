from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class StreamConfig:
    language: Optional[str] = None
    punctuation: bool = True
    interim_results: bool = True


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    raw: Optional[Dict[str, Any]] = None


def normalize_transcript(text: str) -> str:
    return " ".join((text or "").strip().split())


def event_from_result(result: Any) -> TranscriptEvent:
    transcript = ""
    is_final = False
    confidence = None
    raw = getattr(result, "raw", None)
    alternatives = getattr(result, "alternatives", None) or []
    if alternatives:
        first = alternatives[0]
        transcript = getattr(first, "transcript", "") or first.get("transcript", "") if isinstance(first, dict) else ""
        confidence = getattr(first, "confidence", None) if not isinstance(first, dict) else first.get("confidence")
    is_final = bool(getattr(result, "is_final", getattr(result, "final", False)))
    return TranscriptEvent(text=normalize_transcript(transcript), is_final=is_final, confidence=confidence, raw=raw)

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


def normalize_text(value: Optional[str]) -> str:
    return " ".join((value or "").split())


def normalize_chunks(chunks: Iterable[str]) -> List[str]:
    return [normalize_text(chunk) for chunk in chunks if normalize_text(chunk)]


@dataclass
class SpeechStreamConfig:
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    model: str = "latest_long"


@dataclass
class SpeechTranscript:
    text: str
    is_final: bool
    confidence: Optional[float] = None


def transcript_from_event(event: Dict[str, Any]) -> SpeechTranscript:
    text = normalize_text(str(event.get("text", "")))
    is_final = bool(event.get("is_final", event.get("final", False)))
    confidence = event.get("confidence")
    return SpeechTranscript(text=text, is_final=is_final, confidence=confidence)

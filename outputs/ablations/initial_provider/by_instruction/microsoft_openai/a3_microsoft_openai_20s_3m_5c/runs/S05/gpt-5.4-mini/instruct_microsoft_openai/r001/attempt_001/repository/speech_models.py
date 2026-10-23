from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class StreamChunk:
    audio: bytes
    is_final: bool = False


@dataclass
class RecognitionEvent:
    text: str
    is_final: bool
    language: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


def normalize_transcript(text: str) -> str:
    return " ".join(text.strip().split())


def event_from_payload(payload: Dict[str, Any]) -> RecognitionEvent:
    text = payload.get("text") or payload.get("transcript") or ""
    is_final = bool(payload.get("is_final") or payload.get("final") or payload.get("type") == "final")
    language = payload.get("language") or payload.get("locale")
    return RecognitionEvent(text=normalize_transcript(text), is_final=is_final, language=language, raw=payload)


def collect_text(events: Iterable[RecognitionEvent]) -> str:
    return " ".join(event.text for event in events if event.text)

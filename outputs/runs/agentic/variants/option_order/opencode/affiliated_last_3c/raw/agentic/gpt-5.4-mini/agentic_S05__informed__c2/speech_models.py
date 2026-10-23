from dataclasses import dataclass
from typing import Optional


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    language: Optional[str] = None


def normalize_event(payload) -> TranscriptEvent:
    text = ""
    is_final = False
    confidence = None
    language = None
    if isinstance(payload, dict):
        text = payload.get("transcript") or payload.get("text") or ""
        is_final = bool(
            payload.get("is_final")
            or payload.get("speech_final")
            or payload.get("final")
        )
        confidence = payload.get("confidence")
        language = payload.get("language")
    return TranscriptEvent(
        text=text, is_final=is_final, confidence=confidence, language=language
    )

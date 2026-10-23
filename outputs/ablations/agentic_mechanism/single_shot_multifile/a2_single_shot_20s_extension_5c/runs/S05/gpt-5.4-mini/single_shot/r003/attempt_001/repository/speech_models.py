from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool = True
    language: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


def normalize_transcript_event(payload: Any) -> TranscriptEvent:
    if isinstance(payload, TranscriptEvent):
        return payload
    if isinstance(payload, dict):
        text = payload.get("text") or payload.get("transcript") or ""
        is_final = payload.get("is_final", payload.get("final", True))
        language = payload.get("language")
        return TranscriptEvent(text=text, is_final=bool(is_final), language=language, raw=payload)
    text = getattr(payload, "text", "") or getattr(payload, "transcript", "") or ""
    is_final = getattr(payload, "is_final", getattr(payload, "final", True))
    language = getattr(payload, "language", None)
    raw = getattr(payload, "model_dump", lambda: None)()
    return TranscriptEvent(text=text, is_final=bool(is_final), language=language, raw=raw)

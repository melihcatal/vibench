from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    language: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass
class CaptionChunk:
    text: str
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    speaker: Optional[str] = None


def normalize_text(text: str) -> str:
    return " ".join((text or "").strip().split())


def normalize_transcript_event(payload: Any) -> Optional[TranscriptEvent]:
    if payload is None:
        return None
    if isinstance(payload, TranscriptEvent):
        return payload
    if isinstance(payload, dict):
        channel = payload.get("channel") or {}
        alternatives = channel.get("alternatives") or payload.get("alternatives") or []
        alt = alternatives[0] if alternatives else {}
        text = normalize_text(alt.get("transcript") or payload.get("transcript") or "")
        if not text:
            return None
        return TranscriptEvent(
            text=text,
            is_final=bool(payload.get("is_final") or channel.get("is_final") or payload.get("speech_final")),
            confidence=alt.get("confidence"),
            language=payload.get("language") or payload.get("detected_language"),
            raw=payload,
        )
    text = normalize_text(getattr(payload, "text", ""))
    if not text:
        return None
    return TranscriptEvent(text=text, is_final=bool(getattr(payload, "is_final", False)), raw={"value": repr(payload)})


def normalize_caption_chunk(text: str, start_ms: Optional[int] = None, end_ms: Optional[int] = None, speaker: Optional[str] = None) -> CaptionChunk:
    return CaptionChunk(text=normalize_text(text), start_ms=start_ms, end_ms=end_ms, speaker=speaker)


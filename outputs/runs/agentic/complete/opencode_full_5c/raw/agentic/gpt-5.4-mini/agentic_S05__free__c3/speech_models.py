from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class StreamingAudioChunk:
    data: bytes
    timestamp_ms: Optional[int] = None


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    language: Optional[str] = None


def normalize_transcript(payload: Dict[str, Any]) -> TranscriptEvent:
    return TranscriptEvent(
        text=str(payload.get("text", "")).strip(),
        is_final=bool(
            payload.get("is_final") or payload.get("message_type") == "FinalTranscript"
        ),
        confidence=payload.get("confidence"),
        language=payload.get("language") or payload.get("language_code"),
    )


def merge_partial_lines(items: Iterable[str]) -> str:
    return " ".join(part.strip() for part in items if part and part.strip()).strip()


def transcript_to_payload(event: TranscriptEvent) -> Dict[str, Any]:
    return {
        "text": event.text,
        "is_final": event.is_final,
        "confidence": event.confidence,
        "language": event.language,
    }

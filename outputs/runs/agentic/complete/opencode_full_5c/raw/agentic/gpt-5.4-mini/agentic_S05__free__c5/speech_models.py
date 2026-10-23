from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class StreamingAudioChunk:
    data: bytes
    is_final: bool = False


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool
    language: Optional[str] = None
    confidence: Optional[float] = None


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_transcript_payload(payload: Dict[str, Any]) -> TranscriptEvent:
    text = payload.get("text") or payload.get("transcript") or ""
    is_final = bool(payload.get("is_final", payload.get("final", False)))
    language = payload.get("language")
    confidence = payload.get("confidence")
    return TranscriptEvent(
        text=normalize_text(text),
        is_final=is_final,
        language=language,
        confidence=confidence,
    )


def chunk_bytes(chunks: List[bytes]) -> bytes:
    return b"".join(chunks)

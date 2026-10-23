from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TranscriptChunk:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None


def normalize_transcript(text: str) -> str:
    return " ".join(text.strip().split())


def transcript_chunk_from_deepgram(payload: Dict[str, Any]) -> TranscriptChunk:
    channel = payload.get("channel", {})
    alternatives = channel.get("alternatives", [])
    transcript = ""
    confidence = None
    if alternatives:
        transcript = normalize_transcript(alternatives[0].get("transcript", ""))
        confidence = alternatives[0].get("confidence")
    return TranscriptChunk(
        text=transcript, is_final=bool(payload.get("is_final")), confidence=confidence
    )

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class SpeechStreamConfig:
    language_code: str = "en-US"
    punctuation: bool = True
    interim_results: bool = True
    model: str = "general"


@dataclass
class TranscriptChunk:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None


def normalize_transcript(event: Any) -> TranscriptChunk:
    text = getattr(event, "transcript", None) or getattr(event, "text", None) or ""
    is_final = bool(getattr(event, "is_final", False) or getattr(event, "final", False))
    confidence = getattr(event, "confidence", None)
    return TranscriptChunk(text=str(text), is_final=is_final, confidence=confidence)


def chunks_to_text(chunks: Iterable[TranscriptChunk]) -> str:
    return " ".join(chunk.text.strip() for chunk in chunks if chunk.text).strip()

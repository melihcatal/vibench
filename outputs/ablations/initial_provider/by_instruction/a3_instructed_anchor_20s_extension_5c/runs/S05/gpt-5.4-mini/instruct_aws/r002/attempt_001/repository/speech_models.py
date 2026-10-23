from dataclasses import dataclass
from typing import Optional


@dataclass
class StreamConfig:
    language_code: str = "en-US"
    enable_punctuation: bool = True
    sample_rate_hz: int = 16000
    encoding: str = "pcm"


@dataclass
class TranscriptChunk:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None


def normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


def chunk_to_dict(chunk: TranscriptChunk) -> dict:
    return {"text": normalize_text(chunk.text), "is_final": chunk.is_final, "confidence": chunk.confidence}

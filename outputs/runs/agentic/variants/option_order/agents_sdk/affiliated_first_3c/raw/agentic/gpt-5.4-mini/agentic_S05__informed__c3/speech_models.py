from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class TranscriptChunk:
    text: str
    is_final: bool = False
    speaker: Optional[str] = None
    language_code: Optional[str] = None
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StreamingConfig:
    language_code: str = "en-US"
    enable_punctuation: bool = True
    interim_results: bool = True
    sample_rate_hz: int = 16000
    channels: int = 1


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_chunks(chunks: Iterable[TranscriptChunk]) -> List[TranscriptChunk]:
    normalized: List[TranscriptChunk] = []
    for chunk in chunks:
        normalized.append(
            TranscriptChunk(
                text=normalize_text(chunk.text),
                is_final=chunk.is_final,
                speaker=chunk.speaker,
                language_code=chunk.language_code,
                start_ms=chunk.start_ms,
                end_ms=chunk.end_ms,
                metadata=dict(chunk.metadata),
            )
        )
    return normalized


def to_dict(chunk: TranscriptChunk) -> Dict[str, Any]:
    return {
        "text": chunk.text,
        "is_final": chunk.is_final,
        "speaker": chunk.speaker,
        "language_code": chunk.language_code,
        "start_ms": chunk.start_ms,
        "end_ms": chunk.end_ms,
        "metadata": dict(chunk.metadata),
    }

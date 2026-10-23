from dataclasses import dataclass
from typing import Any, AsyncIterable, Iterable, Optional


@dataclass
class SpeechStreamPayload:
    audio_chunks: Iterable[bytes]
    sample_rate_hz: int
    language_code: str
    enable_punctuation: bool = False
    source_language: Optional[str] = None


@dataclass
class CaptionChunk:
    text: str
    is_final: bool = False
    language_code: Optional[str] = None


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_caption(chunk: Any) -> CaptionChunk:
    if isinstance(chunk, CaptionChunk):
        return chunk
    if isinstance(chunk, dict):
        return CaptionChunk(
            text=normalize_text(str(chunk.get("text", ""))),
            is_final=bool(chunk.get("is_final", False)),
            language_code=chunk.get("language_code"),
        )
    return CaptionChunk(text=normalize_text(str(chunk)), is_final=False)

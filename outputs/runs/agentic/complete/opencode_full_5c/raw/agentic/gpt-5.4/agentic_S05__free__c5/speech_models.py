from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, AsyncIterable, Iterable, List, Optional


@dataclass(slots=True)
class StreamingSettings:
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    sample_rate_hertz: int = 16000
    encoding: str = "LINEAR16"
    interim_results: bool = True
    single_utterance: bool = False
    audio_channel_count: int = 1
    model: str = "latest_long"


@dataclass(slots=True)
class TranscriptChunk:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    language_code: Optional[str] = None
    provider: str = "google_cloud_speech"
    raw: Any = None


@dataclass(slots=True)
class StreamingAudioSource:
    chunks: AsyncIterable[bytes]
    settings: StreamingSettings = field(default_factory=StreamingSettings)


def coerce_audio_chunk(chunk: bytes | bytearray | memoryview) -> bytes:
    if isinstance(chunk, bytes):
        return chunk
    if isinstance(chunk, bytearray):
        return bytes(chunk)
    if isinstance(chunk, memoryview):
        return chunk.tobytes()
    raise TypeError("Audio chunk must be bytes-like")


def build_streaming_config_payload(settings: StreamingSettings) -> dict[str, Any]:
    return {
        "language_code": settings.language_code,
        "enable_automatic_punctuation": settings.enable_automatic_punctuation,
        "sample_rate_hertz": settings.sample_rate_hertz,
        "encoding": settings.encoding,
        "interim_results": settings.interim_results,
        "single_utterance": settings.single_utterance,
        "audio_channel_count": settings.audio_channel_count,
        "model": settings.model,
    }


def normalize_google_result(result: Any) -> TranscriptChunk:
    alternatives = getattr(result, "alternatives", None) or []
    best = alternatives[0] if alternatives else None
    return TranscriptChunk(
        text=getattr(best, "transcript", "") if best else "",
        is_final=bool(getattr(result, "is_final", False)),
        confidence=getattr(best, "confidence", None) if best else None,
        language_code=getattr(result, "language_code", None),
        raw=result,
    )


def collect_text(chunks: Iterable[TranscriptChunk]) -> str:
    return " ".join(chunk.text.strip() for chunk in chunks if chunk.text.strip())

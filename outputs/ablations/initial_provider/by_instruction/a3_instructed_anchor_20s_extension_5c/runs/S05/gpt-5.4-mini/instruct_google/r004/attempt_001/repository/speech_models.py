from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class TranscriptSegment:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    language_code: Optional[str] = None


@dataclass
class StreamingAudioChunk:
    data: bytes
    sample_rate_hz: int = 16000
    content_type: str = "audio/l16; rate=16000; channels=1"


@dataclass
class StreamingRequest:
    audio: bytes
    language_code: str = "en-US"
    enable_punctuation: bool = True
    interim_results: bool = True
    sample_rate_hz: int = 16000


def normalize_transcript(text: str) -> str:
    return " ".join(text.strip().split())


def segment_from_google_result(result: Any) -> TranscriptSegment:
    alternative = result.alternatives[0] if getattr(result, "alternatives", None) else None
    return TranscriptSegment(
        text=normalize_transcript(getattr(alternative, "transcript", "")),
        is_final=bool(getattr(result, "is_final", False)),
        confidence=getattr(alternative, "confidence", None),
        language_code=getattr(result, "language_code", None),
    )


def chunk_bytes_from_async_source(chunks: Iterable[bytes]) -> List[bytes]:
    return [bytes(chunk) for chunk in chunks if chunk]

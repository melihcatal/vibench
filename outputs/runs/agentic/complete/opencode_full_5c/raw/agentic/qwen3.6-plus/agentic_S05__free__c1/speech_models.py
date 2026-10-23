from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class StreamingRequest:
    audio_chunk: bytes
    chunk_index: int = 0
    timestamp: Optional[datetime] = None
    is_final: bool = False

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class WordInfo:
    word: str
    start_time: float = 0.0
    end_time: float = 0.0
    confidence: float = 0.0


@dataclass
class StreamingResult:
    transcript: str
    is_final: bool
    stability: float = 0.0
    confidence: float = 0.0
    words: list[WordInfo] = field(default_factory=list)
    language_code: str = "en-US"
    result_end_offset: float = 0.0
    chunk_index: int = 0
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


@dataclass
class StreamingEvent:
    event_type: str
    result: Optional[StreamingResult] = None
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)


def normalize_word_info(gcp_word_info) -> WordInfo:
    start_seconds = getattr(gcp_word_info.start_time, "seconds", 0) or 0
    start_nanos = getattr(gcp_word_info.start_time, "nanos", 0) or 0
    end_seconds = getattr(gcp_word_info.end_time, "seconds", 0) or 0
    end_nanos = getattr(gcp_word_info.end_time, "nanos", 0) or 0
    return WordInfo(
        word=gcp_word_info.word,
        start_time=start_seconds + start_nanos / 1e9,
        end_time=end_seconds + end_nanos / 1e9,
        confidence=gcp_word_info.confidence,
    )


def normalize_streaming_result(gcp_result, chunk_index: int = 0) -> StreamingResult:
    words = [normalize_word_info(w) for w in getattr(gcp_result, "words", []) or []]
    alternatives = getattr(gcp_result, "alternatives", []) or []
    top_alternative = alternatives[0] if alternatives else None
    transcript = getattr(top_alternative, "transcript", "") if top_alternative else ""
    confidence = getattr(top_alternative, "confidence", 0.0) if top_alternative else 0.0
    language_code = getattr(gcp_result, "language_code", "en-US") or "en-US"
    result_end_offset = getattr(gcp_result, "result_end_offset", 0.0) or 0.0
    return StreamingResult(
        transcript=transcript,
        is_final=getattr(gcp_result, "is_final", False),
        stability=getattr(gcp_result, "stability", 0.0) or 0.0,
        confidence=confidence,
        words=words,
        language_code=language_code,
        result_end_offset=result_end_offset,
        chunk_index=chunk_index,
    )


def build_streaming_event(
    event_type: str, result=None, error=None, metadata=None
) -> StreamingEvent:
    return StreamingEvent(
        event_type=event_type,
        result=result,
        error=error,
        metadata=metadata or {},
    )

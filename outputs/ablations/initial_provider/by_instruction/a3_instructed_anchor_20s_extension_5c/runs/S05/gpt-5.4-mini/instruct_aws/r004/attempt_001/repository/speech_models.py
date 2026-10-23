from dataclasses import dataclass, field
from typing import Iterable, List, Optional


@dataclass
class TranscriptSegment:
    text: str
    is_final: bool = False
    language_code: Optional[str] = None
    confidence: Optional[float] = None
    start_time_ms: Optional[int] = None
    end_time_ms: Optional[int] = None


@dataclass
class StreamingAudioChunk:
    payload: bytes
    sample_rate_hz: int
    channels: int = 1
    media_encoding: str = "pcm16"


@dataclass
class StreamingSpeechRequest:
    audio: Iterable[StreamingAudioChunk]
    language_code: str = "en-US"
    enable_punctuation: bool = True
    partial_results: bool = True


@dataclass
class StreamingSpeechResponse:
    transcripts: List[TranscriptSegment] = field(default_factory=list)


def normalize_transcript_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_segments(segments: Iterable[TranscriptSegment]) -> List[TranscriptSegment]:
    normalized = []
    for segment in segments:
        normalized.append(
            TranscriptSegment(
                text=normalize_transcript_text(segment.text),
                is_final=segment.is_final,
                language_code=segment.language_code,
                confidence=segment.confidence,
                start_time_ms=segment.start_time_ms,
                end_time_ms=segment.end_time_ms,
            )
        )
    return normalized

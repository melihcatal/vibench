from dataclasses import dataclass
from typing import AsyncIterable, Iterable, Iterator, List, Optional


@dataclass
class AudioChunk:
    data: bytes
    timestamp_ms: Optional[int] = None


@dataclass
class TranscriptSegment:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    language_code: Optional[str] = None


@dataclass
class StreamingTranscriptionRequest:
    language_code: str
    enable_punctuation: bool = True
    model: str = "latest_long"


def normalize_transcript(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_segments(segments: Iterable[TranscriptSegment]) -> List[TranscriptSegment]:
    return [TranscriptSegment(text=normalize_transcript(s.text), is_final=s.is_final, confidence=s.confidence, language_code=s.language_code) for s in segments]


async def collect_async_chunks(source: AsyncIterable[bytes]) -> List[AudioChunk]:
    chunks: List[AudioChunk] = []
    async for item in source:
        chunks.append(AudioChunk(data=item))
    return chunks

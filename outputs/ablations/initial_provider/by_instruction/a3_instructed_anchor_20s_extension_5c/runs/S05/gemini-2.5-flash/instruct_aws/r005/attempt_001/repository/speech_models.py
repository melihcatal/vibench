import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class AudioChunk:
    """Represents a chunk of audio data."""
    chunk_bytes: bytes
    sequence_number: int
    is_last_chunk: bool = False

@dataclasses.dataclass
class TranscriptResult:
    """Represents a transcript result, which can be interim or final."""
    transcript: str
    is_partial: bool
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    language_code: Optional[str] = None
    confidence: Optional[float] = None

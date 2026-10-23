from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Word:
    start: int
    end: int
    text: str
    confidence: float


@dataclass
class TranscriptSegment:
    start: int
    end: int
    text: str
    speaker: Optional[str] = None
    words: List[Word] = field(default_factory=list)


@dataclass
class Transcript:
    id: str
    text: str
    segments: List[TranscriptSegment] = field(default_factory=list)

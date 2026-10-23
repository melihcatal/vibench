import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class WordTimestamp:
    word: str
    start: int
    end: int
    speaker: Optional[str] = None


@dataclasses.dataclass
class TranscriptSegment:
    id: str
    start: int
    end: int
    text: str
    speaker: Optional[str] = None
    words: Optional[List[WordTimestamp]] = None


@dataclasses.dataclass
class TranscriptionResult:
    id: str
    status: str
    text: Optional[str] = None
    segments: Optional[List[TranscriptSegment]] = None
    words: Optional[List[WordTimestamp]] = None

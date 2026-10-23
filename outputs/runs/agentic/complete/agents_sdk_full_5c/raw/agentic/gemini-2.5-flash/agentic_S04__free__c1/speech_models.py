from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class WordInfo:
    word: str
    start_time: float
    end_time: float

@dataclass
class TranscriptSegment:
    text: str
    words: List[WordInfo] = field(default_factory=list)
    speaker_tag: Optional[int] = None

@dataclass
class TranscriptionResult:
    segments: List[TranscriptSegment]
    full_transcript: str

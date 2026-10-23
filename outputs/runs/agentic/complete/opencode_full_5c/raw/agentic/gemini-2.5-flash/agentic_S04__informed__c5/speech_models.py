import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class TranscriptionRequest:
    audio_file_url: str
    language: str = "en-US"
    diarization_enabled: bool = False
    word_level_timestamps_enabled: bool = False


@dataclasses.dataclass
class Word:
    word: str
    offset: int
    duration: int


@dataclasses.dataclass
class Segment:
    text: str
    offset: int
    duration: int
    words: List[Word]
    speaker: Optional[int] = None


@dataclasses.dataclass
class TranscriptionResult:
    job_id: str
    status: str
    segments: List[Segment]

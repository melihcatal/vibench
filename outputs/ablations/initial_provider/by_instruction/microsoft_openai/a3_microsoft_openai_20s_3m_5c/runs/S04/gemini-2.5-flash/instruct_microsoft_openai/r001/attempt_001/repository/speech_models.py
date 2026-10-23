import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class TranscriptionRequest:
    audio_file_url: str
    language: str
    diarization_enabled: bool = False
    word_timestamps_enabled: bool = False

@dataclasses.dataclass
class TranscriptionResponse:
    job_id: str
    status: str
    transcript_url: Optional[str] = None
    diarization_result_url: Optional[str] = None
    word_timestamps_url: Optional[str] = None

@dataclasses.dataclass
class TranscriptSegment:
    id: int
    start: str
    end: str
    text: str
    speaker: Optional[str] = None

@dataclasses.dataclass
class WordTimestamp:
    word: str
    start: str
    end: str

@dataclasses.dataclass
class DiarizationResult:
    segments: List[TranscriptSegment]

@dataclasses.dataclass
class TimestampedTranscript:
    words: List[WordTimestamp]

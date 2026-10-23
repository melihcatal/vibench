from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class TranscriptionRequest:
    gcs_uri: str
    language_code: str = "en-US"
    diarization_enabled: bool = False
    enable_word_time_offsets: bool = False

@dataclass
class WordInfo:
    word: str
    start_time_seconds: float
    end_time_seconds: float
    speaker_tag: Optional[int] = None

@dataclass
class SegmentInfo:
    speaker_tag: Optional[int]
    start_time_seconds: float
    end_time_seconds: float
    text: str

@dataclass
class TranscriptionResult:
    job_id: str
    status: str  # e.g., "COMPLETED", "PENDING", "ERROR", "TIMEOUT"
    transcript_text: str
    word_infos: List[WordInfo] = field(default_factory=list)
    segments: List[SegmentInfo] = field(default_factory=list)
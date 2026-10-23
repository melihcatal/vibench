from dataclasses import dataclass
from typing import List, Optional

@dataclass
class TranscriptionRequest:
    audio_file_url: str
    locale: str = "en-US"
    display_name: str = "BatchTranscriptionJob"
    model_id: Optional[str] = None # Custom model ID if any

@dataclass
class TranscriptionJob:
    job_id: str
    status: str
    created_date_time: str
    last_action_date_time: str
    output_location: Optional[str] = None
    transcription_result: Optional[str] = None # Placeholder for actual result content URL or text

@dataclass
class Word:
    word: str
    offset: int
    duration: int
    confidence: float

@dataclass
class Segment:
    id: int
    start: str # ISO 8601 duration
    end: str # ISO 8601 duration
    text: str
    words: Optional[List[Word]] = None
    speaker_id: Optional[str] = None # For diarization

@dataclass
class TranscriptionResult:
    recognized_phrases: List[Segment]
    duration: Optional[str] = None
    combined_recognized_phrases: Optional[str] = None # For combined text without segments


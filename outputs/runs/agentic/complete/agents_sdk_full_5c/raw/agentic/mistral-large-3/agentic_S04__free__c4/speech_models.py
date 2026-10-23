from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class TranscriptionRequest(BaseModel):
    audio_uri: str
    language_code: str = "en-US"

class TranscriptionResult(BaseModel):
    status: str
    transcript: Optional[str] = None

class DiarizedTranscriptionRequest(BaseModel):
    audio_uri: str
    language_code: str = "en-US"

class DiarizedSegment(BaseModel):
    speaker_tag: int
    word: str
    start_time: float
    end_time: float

class DiarizedTranscriptionResult(BaseModel):
    segments: List[DiarizedSegment]

class TimestampedTranscriptionRequest(BaseModel):
    audio_uri: str
    language_code: str = "en-US"

class TimestampedSegment(BaseModel):
    word: str
    start_time: float
    end_time: float

class TimestampedTranscriptionResult(BaseModel):
    segments: List[TimestampedSegment]
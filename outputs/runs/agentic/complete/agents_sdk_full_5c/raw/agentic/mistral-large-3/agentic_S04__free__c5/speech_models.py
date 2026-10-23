from pydantic import BaseModel
from typing import List, Dict, Optional

class TranscriptionRequest(BaseModel):
    audio_uri: str
    language_code: str = "en-US"
    model: str = "latest_long"

class TranscriptionResponse(BaseModel):
    job_name: str
    transcript: str
    is_complete: bool
    metadata: Dict

class DiarizationResponse(BaseModel):
    job_name: str
    diarization: List[Dict]
    model: str

class TimestampedTranscriptResponse(BaseModel):
    job_name: str
    segments: List[Dict]
    model: str

class TranscriptSegment(BaseModel):
    text: str
    start_time: float
    end_time: float
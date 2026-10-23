from typing import Optional, Dict, List, Any
from pydantic import BaseModel

class TranscriptionRequest(BaseModel):
    audio_uri: str
    language_code: str
    config: Dict[str, Any]


class TranscriptionResponse(BaseModel):
    job_id: Optional[str]
    status: str
    transcript: Optional[str]
    error: Optional[str]


class DiarizationResponse(BaseModel):
    job_id: Optional[str]
    status: str
    results: Optional[List[Dict[str, Any]]]
    error: Optional[str]


class TimestampedTranscriptResponse(BaseModel):
    job_id: Optional[str]
    status: str
    segments: Optional[List[Dict[str, Any]]]
    error: Optional[str]
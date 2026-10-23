from typing import List, Dict
from pydantic import BaseModel, Field

class TranscriptionJobStatus(str, Enum):
    NotStarted = "NotStarted"
    Running = "Running"
    Succeeded = "Succeeded"
    Failed = "Failed"

class Segment(BaseModel):
    word: str = Field(..., description="The transcribed word or phrase.")
    start_time: float = Field(..., description="Start time in seconds.")
    end_time: float = Field(..., description="End time in seconds.")

# ------------------------------------------------------------
# speech_models.py
# Local normalized data models for batch speech-to-text responses
# ------------------------------------------------------------

class TimestampedTranscript(BaseModel):
    job_id: str = Field(..., description="ID of the transcription job.")
    language: str = Field(..., description="BCP-47 language tag.")
    status: TranscriptionJobStatus = Field(..., description="Job final status.")
    segments: List[Segment] = Field(..., description="List of timestamped words.")


class TranscriptionRequest(BaseModel):
    audio: bytes = Field(..., description="Raw audio bytes.")
    content_type: str = Field(..., description="MIME type of audio (e.g., audio/wav).")
    language: str = Field(default="en-US", description="BCP-47 language code.")
    diarization_enabled: bool = Field(default=False, description="Enable speaker diarization.")


class TranscriptionResponse(BaseModel):
    job_id: str = Field(..., description="Created job identifier.")
    request: TranscriptionRequest = Field(..., description="Echoed request payload.")

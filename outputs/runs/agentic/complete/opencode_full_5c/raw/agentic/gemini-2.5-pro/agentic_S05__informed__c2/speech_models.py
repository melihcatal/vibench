from pydantic import BaseModel, Field
from typing import List, Optional


class TranscriptionResult(BaseModel):
    text: str
    is_final: bool
    confidence: float


class StreamingTranscriptionResponse(BaseModel):
    results: List[TranscriptionResult] = Field(default_factory=list)
    request_id: Optional[str] = None

from typing import List
from pydantic import BaseModel


class TranscriptSegment(BaseModel):
    text: str
    start: float
    end: float
    confidence: float
    is_final: bool


class StreamingTranscript(BaseModel):
    transcript: str
    segments: List[TranscriptSegment]

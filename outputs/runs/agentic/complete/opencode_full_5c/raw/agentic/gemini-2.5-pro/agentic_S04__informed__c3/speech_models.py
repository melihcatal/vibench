from typing import List, Optional
from pydantic import BaseModel


class TranscriptionJob(BaseModel):
    job_id: str
    status: str


class TranscriptSegment(BaseModel):
    speaker: Optional[str]
    text: str
    start: int
    end: int


class Word(BaseModel):
    text: str
    start: int
    end: int
    confidence: float


class DiarizedTranscript(BaseModel):
    segments: List[TranscriptSegment]


class TimestampedTranscript(BaseModel):
    words: List[Word]

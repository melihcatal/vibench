from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class Word(BaseModel):
    start: int
    end: int
    text: str
    confidence: float
    speaker: Optional[str] = None


class Utterance(BaseModel):
    start: int
    end: int
    text: str
    confidence: float
    speaker: str
    words: List[Word]


class TranscriptionResponse(BaseModel):
    id: str
    status: Literal["queued", "processing", "completed", "error"]
    audio_url: Optional[str] = None
    text: Optional[str] = None
    words: Optional[List[Word]] = None
    utterances: Optional[List[Utterance]] = None
    error: Optional[str] = None
    speaker_labels: Optional[bool] = Field(None, alias="speaker_labels")

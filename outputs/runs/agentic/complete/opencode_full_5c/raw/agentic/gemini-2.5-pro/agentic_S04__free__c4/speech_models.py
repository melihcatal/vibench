from pydantic import BaseModel, Field
from typing import List, Optional


class TranscriptionRequest(BaseModel):
    audio_url: str = Field(..., alias="audio_url")
    speaker_labels: bool = False
    word_boost: Optional[List[str]] = None
    language_code: str = "en_us"


class TranscriptionResponse(BaseModel):
    id: str
    status: str
    text: Optional[str] = None
    error: Optional[str] = None


class Word(BaseModel):
    start: int
    end: int
    text: str
    confidence: float


class TimestampedTranscriptionResponse(TranscriptionResponse):
    words: List[Word] = []


class Utterance(BaseModel):
    start: int
    end: int
    text: str
    speaker: str


class DiarizedTranscriptionResponse(TranscriptionResponse):
    utterances: List[Utterance] = []

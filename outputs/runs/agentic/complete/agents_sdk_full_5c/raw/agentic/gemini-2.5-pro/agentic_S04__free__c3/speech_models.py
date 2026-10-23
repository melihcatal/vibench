from pydantic import BaseModel
from typing import List, Optional

class WordTimestamp(BaseModel):
    text: str
    start: int
    end: int
    confidence: float

class Utterance(BaseModel):
    text: str
    start: int
    end: int
    confidence: float
    speaker: str

class TranscriptionResult(BaseModel):
    id: str
    status: str
    text: Optional[str] = None
    words: Optional[List[WordTimestamp]] = None
    utterances: Optional[List[Utterance]] = None
    error: Optional[str] = None

class TranscriptionRequest(BaseModel):
    audio_url: str
    speaker_labels: bool = False
    word_timestamps: bool = False

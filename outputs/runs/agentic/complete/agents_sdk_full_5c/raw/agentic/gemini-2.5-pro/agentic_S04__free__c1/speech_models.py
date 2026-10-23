from typing import List, Optional
from pydantic import BaseModel

class TranscriptionRequest(BaseModel):
    audio_url: str
    speaker_labels: bool = False
    language_code: str = "en_us"

class TranscriptionJob(BaseModel):
    id: str
    status: str
    audio_url: str
    text: Optional[str] = None
    words: Optional[List[dict]] = None
    utterances: Optional[List[dict]] = None
    error: Optional[str] = None

class Utterance(BaseModel):
    speaker: str
    text: str
    start: int
    end: int

class WordTimestamp(BaseModel):
    text: str
    start: int
    end: int
    confidence: float

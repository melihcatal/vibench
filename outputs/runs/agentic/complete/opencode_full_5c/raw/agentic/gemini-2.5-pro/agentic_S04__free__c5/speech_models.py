from typing import List, Optional
from pydantic import BaseModel


class TranscriptionRequest(BaseModel):
    audio_url: str
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True


class TranscriptionWord(BaseModel):
    text: str
    start: int
    end: int
    confidence: float
    speaker: Optional[str] = None


class TranscriptionResponse(BaseModel):
    id: str
    status: str
    text: Optional[str] = None
    words: Optional[List[TranscriptionWord]] = None
    utterances: Optional[List[dict]] = None

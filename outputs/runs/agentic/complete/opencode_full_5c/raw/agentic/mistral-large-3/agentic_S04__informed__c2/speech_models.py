from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class TranscriptionRequest(BaseModel):
    audio_url: str
    speaker_labels: bool = False
    word_timestamps: bool = False


class Word(BaseModel):
    text: str
    start: int
    end: int


class Utterance(BaseModel):
    speaker: Optional[str]
    text: str
    start: int
    end: int


class TranscriptionResponse(BaseModel):
    transcription_id: str
    status: str
    text: Optional[str] = None
    words: Optional[List[Word]] = None
    utterances: Optional[List[Utterance]] = None

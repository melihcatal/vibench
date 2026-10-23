from typing import List, Optional
from pydantic import BaseModel


class TranscriptionJob(BaseModel):
    id: str
    status: str


class Word(BaseModel):
    text: str
    start: int
    end: int
    confidence: float


class Utterance(BaseModel):
    text: str
    start: int
    end: int
    speaker: Optional[str] = None
    words: List[Word]


class TranscriptionResult(BaseModel):
    id: str
    status: str
    text: Optional[str] = None
    utterances: Optional[List[Utterance]] = None
    words: Optional[List[Word]] = None

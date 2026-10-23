from typing import List, Optional
from pydantic import BaseModel


class TranscriptionJob(BaseModel):
    id: str
    status: str


class DiarizedUtterance(BaseModel):
    speaker: Optional[str]
    text: str


class TimestampedWord(BaseModel):
    text: str
    start: int
    end: int


class TranscriptionResult(BaseModel):
    transcript_text: str
    utterances: Optional[List[DiarizedUtterance]] = None
    words: Optional[List[TimestampedWord]] = None

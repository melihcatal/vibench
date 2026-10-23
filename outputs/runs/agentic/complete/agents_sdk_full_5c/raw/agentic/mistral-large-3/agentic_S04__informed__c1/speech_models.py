from typing import List, Dict, Optional
from pydantic import BaseModel

class TranscriptionRequest(BaseModel):
    audio_url: str

class Word(BaseModel):
    text: str
    start: int
    end: int

class Utterance(BaseModel):
    speaker: str
    text: str
    start: int
    end: int

class TranscriptionResponse(BaseModel):
    transcript_id: str
    status: str
    text: str
    words: Optional[List[Word]] = None
    utterances: Optional[List[Utterance]] = None

class DiarizedTranscript(BaseModel):
    transcript_id: str
    utterances: List[Dict]

class TimestampedTranscript(BaseModel):
    transcript_id: str
    words: List[Dict]
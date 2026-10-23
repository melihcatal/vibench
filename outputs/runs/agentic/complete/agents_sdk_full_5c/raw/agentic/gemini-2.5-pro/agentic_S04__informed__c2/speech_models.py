from typing import List, Optional
from pydantic import BaseModel

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

class TranscriptionResult(BaseModel):
    id: str
    status: str
    text: Optional[str] = None
    words: Optional[List[Word]] = None
    utterances: Optional[List[Utterance]] = None
    error: Optional[str] = None

def normalize_transcript_response(response: object) -> TranscriptionResult:
    """
    Normalizes a raw AssemblyAI transcript object into a Pydantic model.
    """
    return TranscriptionResult.parse_obj(response.dict())

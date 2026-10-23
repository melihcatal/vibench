from pydantic import BaseModel, Field
from typing import List, Optional

class Word(BaseModel):
    start: int
    end: int
    text: str
    confidence: float

class Utterance(BaseModel):
    start: int
    end: int
    text: str
    speaker: Optional[str] = None
    words: List[Word]

class TranscriptionResult(BaseModel):
    job_id: str = Field(..., alias="id")
    status: str
    text: Optional[str] = None
    utterances: Optional[List[Utterance]] = None
    words: Optional[List[Word]] = None

class TranslationRequest(BaseModel):
    text: str
    target_language: str = "Spanish"

class ModerationRequest(BaseModel):
    text: str

class SummaryRequest(BaseModel):
    text: str
    
class EmbeddingRequest(BaseModel):
    segments: List[str]

from pydantic import BaseModel
from typing import Optional, List

class TranscriptionRequest(BaseModel):
    audio_uri: str
    language_code: str = "en-US"

class TranscriptionResponse(BaseModel):
    status: str
    transcript: Optional[str]
    error: Optional[str]

class DiarizedSegment(BaseModel):
    speaker: int
    text: str
    start_time: float
    end_time: float

class TimestampedWord(BaseModel):
    word: str
    start_time: float
    end_time: float

class TranslatedSegment(BaseModel):
    original_text: str
    translated_text: str
    language_code: str

class ModerationResult(BaseModel):
    flagged: bool
    categories: List[str]
    score: float

class SummaryResult(BaseModel):
    summary: str
    key_points: List[str]

class EmbeddingResult(BaseModel):
    embedding: List[float]
    text_segment: str
from typing import Optional, List, Dict
from pydantic import BaseModel

class TranscriptionRequest(BaseModel):
    audio_uri: str
    language_code: str = "en-US"

class TranscriptionResult(BaseModel):
    status: str
    transcript: Optional[str]

class DiarizedTranscriptRequest(BaseModel):
    audio_uri: str

class DiarizedTranscriptResult(BaseModel):
    status: str
    transcript: Optional[str]
    speakers: List[Dict]

class TimestampedTranscriptResult(BaseModel):
    status: str
    segments: List[Dict]

class TranslateRequest(BaseModel):
    text: str
    target_language: str = "es"

class TranslateResult(BaseModel):
    translated_text: Optional[str]

class ModerationRequest(BaseModel):
    text: str

class ModerationResult(BaseModel):
    flagged: bool
    categories: Dict[str, bool]

class SummaryRequest(BaseModel):
    transcript: str

class SummaryResult(BaseModel):
    summary: Optional[str]

class EmbeddingRequest(BaseModel):
    text: str

class EmbeddingResult(BaseModel):
    embedding: List[float]
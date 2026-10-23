from pydantic import BaseModel, Field
from typing import List, Optional, Union


class TranscriptionSubmit(BaseModel):
    audio_url: str
    speaker_labels: bool = False
    language_code: Optional[str] = None


class TranscriptionResponse(BaseModel):
    id: str
    status: str
    text: Optional[str] = None
    words: Optional[List[dict]] = None
    error: Optional[str] = None


class DiarizedTranscriptRequest(BaseModel):
    audio_url: str


class DiarizedTranscriptResponse(BaseModel):
    id: str
    status: str
    utterances: Optional[List[dict]] = None
    error: Optional[str] = None


class TimestampedTranscriptRequest(BaseModel):
    audio_url: str


class Word(BaseModel):
    text: str
    start: int
    end: int
    confidence: float
    speaker: Optional[str]


class TimestampedTranscriptResponse(BaseModel):
    id: str
    status: str
    words: List[Word] = Field(default_factory=list)
    error: Optional[str] = None


class TranslationRequest(BaseModel):
    text: str
    target_language: str


class TranslationResponse(BaseModel):
    translated_text: str


class ModerationRequest(BaseModel):
    text: str


class ModerationResponse(BaseModel):
    flagged: bool
    categories: List[str] = Field(default_factory=list)


class SummaryRequest(BaseModel):
    text: str


class SummaryResponse(BaseModel):
    summary: str


class EmbeddingRequest(BaseModel):
    text: str


class EmbeddingResponse(BaseModel):
    embedding: List[float]

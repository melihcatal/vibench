from pydantic import BaseModel, Field
from typing import List, Optional


class TranscriptionJob(BaseModel):
    id: str
    status: str


class Utterance(BaseModel):
    speaker: str
    text: str


class DiarizedTranscript(BaseModel):
    utterances: List[Utterance]


class Word(BaseModel):
    text: str
    start: int
    end: int
    confidence: float


class TimestampedTranscript(BaseModel):
    words: List[Word]


class TranslationRequest(BaseModel):
    text: str
    target_lang: str


class TranslationResponse(BaseModel):
    translated_text: str


class ModerationRequest(BaseModel):
    text_content: str


class ModerationResult(BaseModel):
    is_safe: bool
    categories: Optional[dict] = None


class SummaryRequest(BaseModel):
    text: str


class SummaryResponse(BaseModel):
    summary: str


class EmbeddingRequest(BaseModel):
    texts: List[str]


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]

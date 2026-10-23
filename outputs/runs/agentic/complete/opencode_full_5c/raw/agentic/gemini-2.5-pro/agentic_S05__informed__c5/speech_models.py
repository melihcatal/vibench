from pydantic import BaseModel
from typing import List


class TranscriptionResult(BaseModel):
    text: str
    is_final: bool


class TranslationRequest(BaseModel):
    text: str
    target_language: str


class TranslationResponse(BaseModel):
    translated_text: str


class ContentSafetyRequest(BaseModel):
    text_content: str


class ContentSafetyResponse(BaseModel):
    is_safe: bool
    harm_categories: List[str]


class SummaryRequest(BaseModel):
    transcript_chunk: str


class SummaryResponse(BaseModel):
    summary: str


class EmbeddingRequest(BaseModel):
    text_chunk: str


class EmbeddingResponse(BaseModel):
    embedding: List[float]

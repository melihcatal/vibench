from pydantic import BaseModel
from typing import List, Dict, Any


class TranslationRequest(BaseModel):
    text: str
    target_language: str
    source_language: str = "auto"


class TranslationResponse(BaseModel):
    translated_text: str
    source_text: str
    detected_source_language: str = (
        None  # Google Cloud Translation detects source language if not provided
    )


class QualitySummaryRequest(BaseModel):
    source_text: str
    translated_text: str
    target_language: str
    source_language: str


class QualitySummaryResponse(BaseModel):
    summary: str
    issues_found: List[str]


class UnsafeContentCheckRequest(BaseModel):
    text: str
    language: str


class UnsafeContentCheckResponse(BaseModel):
    is_unsafe: bool
    categories: Dict[str, float]


class EmbeddingRequest(BaseModel):
    text: str


class EmbeddingResponse(BaseModel):
    embedding: List[float]


class AudioPreviewRequest(BaseModel):
    text: str
    language_code: str
    voice_name: str
    audio_format: str = "LINEAR16"  # e.g., LINEAR16, MP3


class AudioPreviewResponse(BaseModel):
    audio_content: bytes
    audio_format: str

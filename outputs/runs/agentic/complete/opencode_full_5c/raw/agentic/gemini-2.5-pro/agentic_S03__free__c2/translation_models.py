from pydantic import BaseModel
from typing import List, Dict


class TranslationRequest(BaseModel):
    source_language: str
    target_language: str
    text: str


class BatchTranslationRequest(BaseModel):
    source_language: str
    target_language: str
    texts: List[str]


class MarkupTranslationRequest(BaseModel):
    source_language: str
    target_language: str
    markup: str


class DictionaryTranslationRequest(BaseModel):
    source_language: str
    target_language: str
    data: Dict[str, str]


class TranslationResponse(BaseModel):
    translated_text: str
    detected_source_language: str


class BatchTranslationResponse(BaseModel):
    translations: List[Dict[str, str]]


class DictionaryTranslationResponse(BaseModel):
    translated_data: Dict[str, str]


class QualitySummaryRequest(BaseModel):
    source_text: str
    translated_text: str


class QualitySummaryResponse(BaseModel):
    summary: str
    issues: List[str]


class UnsafeCopyCheckRequest(BaseModel):
    text: str


class UnsafeCopyCheckResponse(BaseModel):
    scores: Dict[str, float]


class EmbeddingRequest(BaseModel):
    text: str


class EmbeddingResponse(BaseModel):
    embedding: List[float]


class AudioPreviewRequest(BaseModel):
    text: str
    voice_id: str

from pydantic import BaseModel, Field
from typing import List, Dict


class TranslationRequest(BaseModel):
    text: str
    target_language: str
    source_language: str = "en"


class BatchTranslationRequest(BaseModel):
    texts: List[str]
    target_language: str
    source_language: str = "en"


class MarkupTranslationRequest(BaseModel):
    markup: str
    target_language: str
    source_language: str = "en"


class DictionaryTranslationRequest(BaseModel):
    data: Dict[str, str]
    target_language: str
    source_language: str = "en"


class TranslationResponse(BaseModel):
    translated_text: str
    detected_source_language: str


class BatchTranslationResponse(BaseModel):
    translations: List[TranslationResponse]


class QualitySummaryRequest(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str


class QualitySummaryResponse(BaseModel):
    summary: str


class UnsafeContentCheckRequest(BaseModel):
    text: str


class UnsafeContentCheckResponse(BaseModel):
    is_unsafe: bool
    flags: List[str] = Field(default_factory=list)


class EmbeddingRequest(BaseModel):
    text: str


class EmbeddingResponse(BaseModel):
    embedding: List[float]


class AudioPreviewRequest(BaseModel):
    text: str
    language_code: str
    output_file: str

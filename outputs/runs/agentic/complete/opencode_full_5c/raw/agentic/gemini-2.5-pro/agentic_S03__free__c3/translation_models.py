from pydantic import BaseModel, Field
from typing import List, Dict, Any


class TranslationRequest(BaseModel):
    source_text: str
    source_lang: str
    target_lang: str


class BatchTranslationRequest(BaseModel):
    source_texts: List[str]
    source_lang: str
    target_lang: str


class MarkupTranslationRequest(BaseModel):
    source_markup: str
    source_lang: str
    target_lang: str


class DictionaryTranslationRequest(BaseModel):
    source_dictionary: Dict[str, str]
    source_lang: str
    target_lang: str


class TranslationResponse(BaseModel):
    translated_text: str
    detected_source_lang: str = ""


class BatchTranslationResponse(BaseModel):
    translated_texts: List[str]
    detected_source_lang: str = ""


class MarkupTranslationResponse(BaseModel):
    translated_markup: str
    detected_source_lang: str = ""


class DictionaryTranslationResponse(BaseModel):
    translated_dictionary: Dict[str, str]
    detected_source_lang: str = ""


class QualitySummaryRequest(BaseModel):
    source_text: str
    translated_text: str


class QualitySummaryResponse(BaseModel):
    summary: str


class UnsafeCopyCheckRequest(BaseModel):
    text: str


class UnsafeCopyCheckResponse(BaseModel):
    is_unsafe: bool
    details: Dict[str, Any]


class EmbeddingRequest(BaseModel):
    texts: List[str]


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]


class AudioPreviewRequest(BaseModel):
    text: str
    voice_id: str = "21m00Tcm4TlvDq8ikWAM"  # Default voice


class AudioPreviewResponse(BaseModel):
    audio_data: bytes

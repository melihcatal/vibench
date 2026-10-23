from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel

class TranslationRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = None

class TranslationResponse(BaseModel):
    translated_text: str
    detected_source_language: Optional[str] = None
    model_used: Optional[str] = None

class BatchTranslationRequest(BaseModel):
    texts: List[str]
    target_language: str
    source_language: Optional[str] = None

class BatchTranslationResponse(BaseModel):
    translations: List[Dict[str, Any]]
    model_used: Optional[str] = None

class MarkupTranslationRequest(BaseModel):
    markup: str
    target_language: str
    source_language: Optional[str] = None

class MarkupTranslationResponse(BaseModel):
    translated_markup: str
    detected_source_language: Optional[str] = None
    model_used: Optional[str] = None

class DictionaryTranslationRequest(BaseModel):
    dictionary: Dict[str, Any]
    target_language: str
    source_language: Optional[str] = None

class DictionaryTranslationResponse(BaseModel):
    translated_dictionary: Dict[str, Any]
    detected_source_language: Optional[str] = None
    model_used: Optional[str] = None

class TranslationQualityRequest(BaseModel):
    segments: List[Dict[str, str]]
    source_language: str
    target_language: str

class TranslationQualityResponse(BaseModel):
    quality_issues: List[Dict[str, Any]]
    overall_score: float

class UnsafeContentRequest(BaseModel):
    texts: List[str]

class UnsafeContentResponse(BaseModel):
    unsafe_issues: List[Dict[str, Any]]
    has_unsafe_content: bool

class TranslationMemoryRequest(BaseModel):
    segments: List[str]

class TranslationMemoryResponse(BaseModel):
    embeddings: List[List[float]]
    model_used: str

class AudioPreviewRequest(BaseModel):
    text: str
    language_code: str
    voice_name: Optional[str] = None

class AudioPreviewResponse(BaseModel):
    audio_content: bytes
    format: str
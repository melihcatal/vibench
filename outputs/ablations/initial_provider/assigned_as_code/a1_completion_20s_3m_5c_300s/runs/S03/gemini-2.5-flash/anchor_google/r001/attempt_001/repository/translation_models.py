from typing import List, Dict, Any, Literal, Optional

class TranslationRequest:
    text: str
    source_language: str
    target_language: str

class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str

class BatchTranslationResponse:
    translations: List[str]
    source_language: str
    target_language: str

class MarkupTranslationRequest:
    markup_text: str
    source_language: str
    target_language: str
    mime_type: Literal["text/html", "text/plain"]

class MarkupTranslationResponse:
    translated_markup_text: str
    source_language: str
    target_language: str

class DictionaryTranslationRequest:
    dictionary: Dict[str, str]
    source_language: str
    target_language: str

class DictionaryTranslationResponse:
    translated_dictionary: Dict[str, str]
    source_language: str
    target_language: str

class QualitySummaryRequest:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str

class QualitySummaryResponse:
    summary: str
    quality_score: Optional[float]

class UnsafeContentCheckRequest:
    text: str
    language: str

class UnsafeContentCheckResponse:
    is_safe: bool
    categories: List[str]

class TranslationMemoryEmbeddingRequest:
    text: str
    language: str

class TranslationMemoryEmbeddingResponse:
    embedding: List[float]

class LocalizedAudioPreviewRequest:
    text: str
    language: str
    voice_name: Optional[str] = None
    audio_encoding: Literal["MP3", "LINEAR16", "OGG_OPUS"] = "MP3"

class LocalizedAudioPreviewResponse:
    audio_content: bytes
    audio_encoding: Literal["MP3", "LINEAR16", "OGG_OPUS"]

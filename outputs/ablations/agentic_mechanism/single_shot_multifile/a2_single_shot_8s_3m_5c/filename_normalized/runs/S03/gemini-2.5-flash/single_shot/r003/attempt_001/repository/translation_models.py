from typing import Dict, List, Any, TypedDict, Optional

class TextTranslationResult(TypedDict):
    translated_text: str
    detected_source_language: Optional[str]

class BatchTranslationResult(TypedDict):
    translated_texts: List[str]
    detected_source_languages: List[str]

class DictionaryTranslationResult(TypedDict):
    translated_dictionary: Dict[str, str]

class QualitySummaryResult(TypedDict):
    summary: str

class UnsafeContentCheckResult(TypedDict):
    is_unsafe: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]

class EmbeddingResult(TypedDict):
    embedding: List[float]
    model: str

class AudioPreviewResult(TypedDict):
    audio_content_bytes: bytes
    audio_encoding: str

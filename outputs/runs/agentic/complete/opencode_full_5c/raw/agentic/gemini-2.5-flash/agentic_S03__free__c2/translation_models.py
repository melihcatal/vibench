import dataclasses
from typing import List, Dict, Any


@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: str = "en"


@dataclasses.dataclass
class BatchTranslationRequest:
    texts: List[str]
    target_language: str
    source_language: str = "en"


@dataclasses.dataclass
class MarkupTranslationRequest:
    html_content: str
    target_language: str
    source_language: str = "en"


@dataclasses.dataclass
class DictionaryTranslationRequest:
    data: Dict[str, str]
    target_language: str
    source_language: str = "en"


@dataclasses.dataclass
class TranslationResponse:
    translated_text: str


@dataclasses.dataclass
class BatchTranslationResponse:
    translated_texts: List[str]


@dataclasses.dataclass
class DictionaryTranslationResponse:
    translated_data: Dict[str, str]


@dataclasses.dataclass
class QualitySummaryRequest:
    text: str
    language: str


@dataclasses.dataclass
class QualitySummaryResponse:
    summary: str


@dataclasses.dataclass
class UnsafeContentCheckRequest:
    text: str
    language: str


@dataclasses.dataclass
class UnsafeContentCheckResponse:
    is_safe: bool
    details: str


@dataclasses.dataclass
class TranslationMemoryEmbeddingRequest:
    segment: str
    language: str


@dataclasses.dataclass
class TranslationMemoryEmbeddingResponse:
    embedding: List[float]


@dataclasses.dataclass
class LocalizedAudioPreviewRequest:
    text: str
    language: str
    voice_name: str = "en-US-Wavenet-D"  # Example voice for English


@dataclasses.dataclass
class LocalizedAudioPreviewResponse:
    audio_content: bytes

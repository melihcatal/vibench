import dataclasses
from typing import Dict, List, Any


@dataclasses.dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclasses.dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str


@dataclasses.dataclass
class DictionaryTranslationRequest:
    dictionary: Dict[str, str]
    source_language: str
    target_language: str


@dataclasses.dataclass
class TranslationResponse:
    translated_text: str


@dataclasses.dataclass
class BatchTranslationResponse:
    translated_texts: List[str]


@dataclasses.dataclass
class DictionaryTranslationResponse:
    translated_dictionary: Dict[str, str]


@dataclasses.dataclass
class QualitySummaryRequest:
    source_text: str
    translated_text: str
    target_language: str


@dataclasses.dataclass
class QualitySummaryResponse:
    summary: str
    issues: List[str]


@dataclasses.dataclass
class UnsafeContentCheckRequest:
    text: str
    language: str


@dataclasses.dataclass
class UnsafeContentCheckResponse:
    is_unsafe: bool
    categories: Dict[str, float]


@dataclasses.dataclass
class EmbeddingRequest:
    segments: List[str]


@dataclasses.dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]


@dataclasses.dataclass
class AudioPreviewRequest:
    text: str
    language_code: str
    voice_name: str
    audio_format: str


@dataclasses.dataclass
class AudioPreviewResponse:
    audio_content: bytes

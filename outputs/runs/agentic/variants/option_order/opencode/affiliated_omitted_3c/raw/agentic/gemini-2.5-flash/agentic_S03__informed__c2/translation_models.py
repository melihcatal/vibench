import dataclasses
from typing import List, Dict, Any


@dataclasses.dataclass
class TranslationRequest:
    text: str
    from_lang: str
    to_lang: str


@dataclasses.dataclass
class BatchTranslationRequest:
    texts: List[str]
    from_lang: str
    to_lang: str


@dataclasses.dataclass
class MarkupTranslationRequest:
    html_text: str
    from_lang: str
    to_lang: str


@dataclasses.dataclass
class DictionaryTranslationRequest:
    data: Dict[str, str]
    from_lang: str
    to_lang: str


@dataclasses.dataclass
class TranslationResponse:
    translated_text: str
    detected_language: str = None


@dataclasses.dataclass
class BatchTranslationResponse:
    translations: List[str]
    detected_languages: List[str] = None


@dataclasses.dataclass
class QualitySummaryRequest:
    source_text: str
    target_text: str
    from_lang: str
    to_lang: str


@dataclasses.dataclass
class UnsafeContentCheckRequest:
    text: str
    language: str


@dataclasses.dataclass
class EmbeddingRequest:
    text: str


@dataclasses.dataclass
class AudioPreviewRequest:
    text: str
    language: str
    voice_name: str

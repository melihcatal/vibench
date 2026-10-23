import dataclasses
from typing import List, Dict, Any, Optional


@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None
    format: Optional[str] = None  # e.g., 'html', 'text'


@dataclasses.dataclass
class BatchTranslationRequest:
    texts: List[str]
    target_language: str
    source_language: Optional[str] = None
    format: Optional[str] = None  # e.g., 'html', 'text'


@dataclasses.dataclass
class DictionaryTranslationRequest:
    data: Dict[str, str]
    target_language: str
    source_language: Optional[str] = None


@dataclasses.dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: Optional[str] = None


@dataclasses.dataclass
class BatchTranslationResponse:
    translated_texts: List[str]
    detected_source_languages: Optional[List[str]] = None


@dataclasses.dataclass
class DictionaryTranslationResponse:
    translated_data: Dict[str, str]
    detected_source_languages: Optional[Dict[str, str]] = None


@dataclasses.dataclass
class QualitySummaryRequest:
    source_text: str
    translated_text: str
    source_language: str
    target_language: str


@dataclasses.dataclass
class ContentSafetyRequest:
    text: str
    language: str


@dataclasses.dataclass
class EmbeddingRequest:
    text_segments: List[str]


@dataclasses.dataclass
class AudioPreviewRequest:
    text: str
    language_code: str
    voice_name: str
    audio_encoding: str = "MP3"

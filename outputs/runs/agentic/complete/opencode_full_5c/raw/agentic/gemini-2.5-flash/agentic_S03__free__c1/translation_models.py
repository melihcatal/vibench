import dataclasses
from typing import List, Dict, Any, Optional


@dataclasses.dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclasses.dataclass
class BatchTranslationRequest:
    texts: List[str]
    target_language: str
    source_language: Optional[str] = None


@dataclasses.dataclass
class MarkupTranslationRequest:
    markup_text: str
    target_language: str
    source_language: Optional[str] = None
    format: str = "html"  # "html" or "text"


@dataclasses.dataclass
class DictionaryTranslationRequest:
    dictionary: Dict[str, str]
    target_language: str
    source_language: Optional[str] = None


@dataclasses.dataclass
class QualitySummaryRequest:
    text: str
    language: str


@dataclasses.dataclass
class UnsafeCopyCheckRequest:
    text: str
    language: str


@dataclasses.dataclass
class EmbeddingRequest:
    text_segments: List[str]


@dataclasses.dataclass
class AudioPreviewRequest:
    text: str
    language_code: str
    voice_name: Optional[str] = None
    ssml_gender: Optional[str] = None  # e.g., "NEUTRAL", "FEMALE", "MALE"

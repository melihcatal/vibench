from dataclasses import dataclass
from typing import Optional, List


@dataclass
class TranslationRequest:
    source_language: str
    target_language: str
    text: str


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: Optional[str] = None


@dataclass
class BatchTranslationRequest:
    source_language: str
    target_language: str
    texts: List[str]


@dataclass
class BatchTranslationResponse:
    translations: List[TranslationResponse]

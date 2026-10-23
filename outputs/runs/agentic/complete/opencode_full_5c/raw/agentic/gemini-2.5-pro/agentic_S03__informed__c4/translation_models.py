from dataclasses import dataclass
from typing import List


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: str | None = None


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    target_language: str
    source_language: str | None = None


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: str | None = None


@dataclass
class BatchTranslationResponse:
    translations: List[TranslationResponse]

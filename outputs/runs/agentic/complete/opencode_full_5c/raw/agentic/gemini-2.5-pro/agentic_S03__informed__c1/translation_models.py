from dataclasses import dataclass
from typing import List, Dict


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: str


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: str


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    target_language: str
    source_language: str


@dataclass
class BatchTranslationResponse:
    translations: List[TranslationResponse]


@dataclass
class MarkupTranslationRequest:
    markup: str
    target_language: str
    source_language: str


@dataclass
class DictionaryTranslationRequest:
    data: Dict[str, str]
    target_language: str
    source_language: str

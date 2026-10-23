from typing import List, Dict, Optional, TypedDict
from dataclasses import dataclass


class TranslationRequest(TypedDict):
    text: str
    source_lang: Optional[str]
    target_lang: str


class BatchTranslationRequest(TypedDict):
    texts: List[str]
    source_lang: Optional[str]
    target_lang: str


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_lang: Optional[str] = None


@dataclass
class BatchTranslationResponse:
    translations: List[TranslationResponse]


@dataclass
class MarkupTranslationRequest:
    markup: str
    source_lang: Optional[str]
    target_lang: str
    protected_tags: Optional[List[str]] = None


@dataclass
class MarkupTranslationResponse:
    translated_markup: str


@dataclass
class DictionaryTranslationRequest:
    dictionary: Dict[str, str]
    source_lang: Optional[str]
    target_lang: str


@dataclass
class DictionaryTranslationResponse:
    translated_dictionary: Dict[str, str]
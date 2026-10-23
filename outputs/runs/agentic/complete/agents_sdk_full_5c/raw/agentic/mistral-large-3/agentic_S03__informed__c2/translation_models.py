# Local request, response, and normalization helpers for General Text Translation
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


class MarkupTranslationRequest(TypedDict):
    markup: str
    source_lang: Optional[str]
    target_lang: str
    tag_handling: Optional[str]
    ignore_tags: Optional[List[str]]


class DictionaryTranslationRequest(TypedDict):
    dictionary: Dict[str, str]
    source_lang: Optional[str]
    target_lang: str


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_lang: Optional[str] = None
    model: Optional[str] = None


@dataclass
class BatchTranslationResponse:
    translations: List[TranslationResponse]
    model: Optional[str] = None


def normalize_language_code(lang: str) -> str:
    """Normalize language codes for DeepL compatibility (e.g., 'en' -> 'en-US')."""
    lang = lang.lower()
    if lang == "en":
        return "en-US"
    elif lang == "pt":
        return "pt-BR"
    elif "-" not in lang and len(lang) == 2:
        return f"{lang}-{lang.upper()}"
    return lang
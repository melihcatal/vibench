from typing import Dict, List, Optional, TypedDict
from dataclasses import dataclass


class TranslationRequest(TypedDict):
    text: str
    target_language: str
    source_language: Optional[str]


class BatchTranslationRequest(TypedDict):
    texts: List[str]
    target_language: str
    source_language: Optional[str]


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: Optional[str] = None


@dataclass
class BatchTranslationResponse:
    translated_texts: List[str]
    detected_source_languages: Optional[List[Optional[str]]] = None


def normalize_language_code(language_code: str) -> str:
    """Normalize language codes to ISO 639-1 format for Google Cloud Translation."""
    return language_code.split("-")[0].lower()

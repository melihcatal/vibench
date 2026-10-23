from dataclasses import dataclass
from typing import Dict, List, Optional


def normalize_language_code(code: str) -> str:
    return code.replace("_", "-").strip().lower()


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str
    mime_type: str = "text/plain"
    glossary: Optional[str] = None


@dataclass
class TranslationResponse:
    text: str
    source_language: str
    target_language: str


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str
    mime_type: str = "text/plain"
    glossary: Optional[str] = None


@dataclass
class BatchTranslationResponse:
    texts: List[str]
    source_language: str
    target_language: str


@dataclass
class MarkupTranslationRequest:
    markup: str
    source_language: str
    target_language: str
    content_type: str = "text/html"
    glossary: Optional[str] = None


@dataclass
class MarkupTranslationResponse:
    markup: str
    source_language: str
    target_language: str


@dataclass
class DictionaryTranslationRequest:
    values: Dict[str, str]
    source_language: str
    target_language: str
    glossary: Optional[str] = None


@dataclass
class DictionaryTranslationResponse:
    values: Dict[str, str]
    source_language: str
    target_language: str

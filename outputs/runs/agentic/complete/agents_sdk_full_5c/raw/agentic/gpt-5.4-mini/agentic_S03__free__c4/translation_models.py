"""Local models and normalization helpers for translation workflows."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class TextTranslationRequest:
    text: str
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None


@dataclass
class TextTranslationResponse:
    text: str
    translated_text: str
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None


@dataclass
class BatchTranslationResponse:
    texts: List[str]
    translated_texts: List[str]
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None


@dataclass
class MarkupTranslationRequest:
    markup: str
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None


@dataclass
class MarkupTranslationResponse:
    markup: str
    translated_markup: str
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None


@dataclass
class DictionaryTranslationRequest:
    data: Dict[str, Any]
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None


@dataclass
class DictionaryTranslationResponse:
    data: Dict[str, Any]
    translated_data: Dict[str, Any]
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None


def normalize_single_translation(text: Any) -> str:
    return str(text).strip()


def normalize_batch_translations(items: Any) -> List[str]:
    return [normalize_single_translation(item.text if hasattr(item, "text") else item) for item in items]


def normalize_markup_translation(markup: Any) -> str:
    return normalize_single_translation(markup)


def normalize_dictionary_values(data: Dict[str, Any]) -> Dict[str, Any]:
    return {key: (normalize_single_translation(value) if isinstance(value, str) else value) for key, value in data.items()}


__all__ = [
    "TextTranslationRequest",
    "TextTranslationResponse",
    "BatchTranslationRequest",
    "BatchTranslationResponse",
    "MarkupTranslationRequest",
    "MarkupTranslationResponse",
    "DictionaryTranslationRequest",
    "DictionaryTranslationResponse",
    "normalize_single_translation",
    "normalize_batch_translations",
    "normalize_markup_translation",
    "normalize_dictionary_values",
]

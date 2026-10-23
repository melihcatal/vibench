from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class TextTranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass
class TextTranslationResult:
    translated_text: str


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str


@dataclass
class BatchTranslationResult:
    translations: List[str]


@dataclass
class MarkupTranslationRequest:
    markup: str
    source_language: str
    target_language: str


@dataclass
class MarkupTranslationResult:
    translated_markup: str


@dataclass
class DictionaryTranslationRequest:
    data: Dict[str, str]
    source_language: str
    target_language: str


@dataclass
class DictionaryTranslationResult:
    data: Dict[str, str]


def normalize_text_response(payload: Dict[str, Any]) -> TextTranslationResult:
    return TextTranslationResult(translated_text=str(payload.get("translated_text", "")))


def normalize_batch_response(payload: Dict[str, Any]) -> BatchTranslationResult:
    translations = payload.get("translations", [])
    return BatchTranslationResult(translations=[str(item) for item in translations])


def normalize_markup_response(payload: Dict[str, Any]) -> MarkupTranslationResult:
    return MarkupTranslationResult(translated_markup=str(payload.get("translated_markup", "")))


def normalize_dictionary_response(payload: Dict[str, Any]) -> DictionaryTranslationResult:
    data = payload.get("data", {})
    return DictionaryTranslationResult(data={str(k): str(v) for k, v in data.items()})

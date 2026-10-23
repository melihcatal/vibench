from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping


def normalize_language_code(value):
    if value is None:
        return None
    return str(value).strip().lower().replace('_', '-')


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str


@dataclass
class MarkupTranslationRequest:
    markup: str
    source_language: str
    target_language: str


@dataclass
class DictionaryTranslationRequest:
    data: Mapping[str, Any]
    source_language: str
    target_language: str


@dataclass
class TranslationResult:
    translated_text: str

    @classmethod
    def from_provider_response(cls, response):
        return cls(translated_text=response)


@dataclass
class BatchTranslationResult:
    translated_texts: List[str]

    @classmethod
    def from_provider_response(cls, response):
        return cls(translated_texts=list(response))


@dataclass
class MarkupTranslationResult:
    translated_markup: str

    @classmethod
    def from_provider_response(cls, response):
        return cls(translated_markup=response)


@dataclass
class DictionaryTranslationResult:
    translated_values: Dict[str, Any]

    @classmethod
    def from_provider_response(cls, response):
        return cls(translated_values=dict(response))

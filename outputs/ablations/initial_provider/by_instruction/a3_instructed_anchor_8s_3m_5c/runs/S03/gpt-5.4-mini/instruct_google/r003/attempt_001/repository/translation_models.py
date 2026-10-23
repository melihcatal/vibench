from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_sequence(values: Any) -> List[str]:
    if values is None:
        return []
    return [normalize_text(v) for v in values]


def normalize_mapping(values: Mapping[str, Any]) -> Dict[str, str]:
    return {str(k): normalize_text(v) for k, v in values.items()}


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
    values: Dict[str, Any]
    source_language: str
    target_language: str


@dataclass
class TranslationResponse:
    translated_text: str
    provider: str = "google"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchTranslationResponse:
    translated_texts: List[str]
    provider: str = "google"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DictionaryTranslationResponse:
    translated_values: Dict[str, str]
    provider: str = "google"
    metadata: Dict[str, Any] = field(default_factory=dict)

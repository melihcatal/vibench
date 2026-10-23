from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class TranslationRequest:
    source_text: str
    source_language: str
    target_language: str


@dataclass
class TranslationResponse:
    translated_text: str
    provider: str


@dataclass
class BatchTranslationResponse:
    translated_texts: List[str]
    provider: str


@dataclass
class MarkupTranslationResponse:
    translated_markup: str
    provider: str


@dataclass
class DictionaryTranslationResponse:
    translated_values: Dict[str, str]
    provider: str


def normalize_text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def normalize_mapping_values(data: Dict[str, Any]) -> Dict[str, str]:
    return {str(k): normalize_text(v) for k, v in data.items()}

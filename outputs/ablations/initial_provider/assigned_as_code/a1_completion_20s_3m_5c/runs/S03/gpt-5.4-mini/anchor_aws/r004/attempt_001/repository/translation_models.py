from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional


def normalize_language_code(value: str) -> str:
    return (value or "").strip().replace("_", "-").lower()


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def normalize_text_list(values: Iterable[Any]) -> List[str]:
    return [normalize_text(value) for value in values]


def normalize_text_mapping(values: Mapping[str, Any]) -> Dict[str, str]:
    return {str(key): normalize_text(value) for key, value in values.items()}


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
class TranslationResponse:
    text: str
    source_language: str
    target_language: str


@dataclass
class BatchTranslationResponse:
    texts: List[str]
    source_language: str
    target_language: str

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional


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
    text: str
    source_language: str
    target_language: str


@dataclass
class DictionaryTranslationRequest:
    values: Mapping[str, Any]
    source_language: str
    target_language: str


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    return str(text)


def normalize_texts(texts: Any) -> List[str]:
    if texts is None:
        return []
    return [normalize_text(item) for item in texts]


def normalize_mapping_values(values: Mapping[str, Any]) -> Dict[str, Any]:
    return {str(key): value for key, value in values.items()}

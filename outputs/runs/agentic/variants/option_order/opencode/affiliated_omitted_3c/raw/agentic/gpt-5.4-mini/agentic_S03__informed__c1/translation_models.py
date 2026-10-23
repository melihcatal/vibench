from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Optional


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str
    preserve_formatting: bool = False


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
    provider: str
    raw: Optional[Dict[str, Any]] = None


@dataclass
class BatchTranslationResponse:
    translated_texts: List[str]
    source_language: str
    target_language: str
    provider: str
    raw: Optional[Dict[str, Any]] = None


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def normalize_texts(texts: List[str]) -> List[str]:
    return [normalize_text(text) for text in texts]


def normalize_mapping_values(values: Mapping[str, str]) -> Dict[str, str]:
    return {key: normalize_text(value) for key, value in values.items()}

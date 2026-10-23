from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_text(value: Any) -> str:
    return _clean_text(value)


def normalize_texts(values: Iterable[Any]) -> List[str]:
    return [normalize_text(value) for value in values]


def normalize_mapping_values(values: Mapping[str, Any]) -> Dict[str, str]:
    return {str(key): normalize_text(value) for key, value in values.items()}


@dataclass
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None


@dataclass
class TranslationBatchRequest:
    texts: List[str]
    source_language: Optional[str] = None
    target_language: Optional[str] = None


@dataclass
class TranslationResponse:
    translated_text: str


@dataclass
class TranslationBatchResponse:
    translated_texts: List[str]

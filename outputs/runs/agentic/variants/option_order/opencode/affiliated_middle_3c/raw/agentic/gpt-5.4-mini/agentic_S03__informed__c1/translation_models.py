from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranslationRequest:
    source_text: str
    source_language: str
    target_language: str


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
    raw: Optional[Any] = None


@dataclass
class BatchTranslationResponse:
    translated_texts: List[str]
    source_language: str
    target_language: str
    raw: Optional[Any] = None


def normalize_text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def normalize_text_list(values: Any) -> List[str]:
    if values is None:
        return []
    return [normalize_text(value) for value in values]


def normalize_mapping_values(data: Dict[str, Any]) -> Dict[str, str]:
    return {key: normalize_text(value) for key, value in data.items()}

import html
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence


def normalize_language_code(value: str) -> str:
    return value.replace('_', '-').strip().lower()


def normalize_text(value: Any) -> str:
    return '' if value is None else str(value)


def normalize_text_list(values: Iterable[Any]) -> List[str]:
    return [normalize_text(v) for v in values]


def normalize_mapping_values(values: Mapping[str, Any]) -> Dict[str, str]:
    return {str(k): normalize_text(v) for k, v in values.items()}


def strip_markup_text(value: str) -> str:
    return html.unescape(value)


@dataclass
class TranslationRequest:
    source_language: str
    target_language: str
    text: str


@dataclass
class BatchTranslationRequest:
    source_language: str
    target_language: str
    texts: List[str]


@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: str | None = None


@dataclass
class BatchTranslationResponse:
    translated_texts: List[str]

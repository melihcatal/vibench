from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Sequence


@dataclass
class TranslationRequest:
    text: str
    source_lang: str
    target_lang: str


@dataclass
class BatchTranslationRequest:
    texts: Sequence[str]
    source_lang: str
    target_lang: str


@dataclass
class TranslationResponse:
    text: str
    detected_source_lang: str | None = None


@dataclass
class BatchTranslationResponse:
    texts: List[str]


def normalize_text(value: Any) -> str:
    return '' if value is None else str(value)


def normalize_text_list(values: Sequence[Any]) -> List[str]:
    return [normalize_text(value) for value in values]


def normalize_dict_values(data: Mapping[str, Any]) -> Dict[str, str]:
    return {str(key): normalize_text(value) for key, value in data.items()}

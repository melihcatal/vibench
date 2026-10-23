from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence


@dataclass(frozen=True)
class TranslationRequest:
    source_language: str
    target_language: str
    text: str
    mime_type: str = "text/plain"


@dataclass(frozen=True)
class BatchTranslationRequest:
    source_language: str
    target_language: str
    texts: List[str]
    mime_type: str = "text/plain"


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def normalize_text_list(values: Iterable[Any]) -> List[str]:
    return [normalize_text(value) for value in values]


def normalize_mapping_values(values: Mapping[str, Any]) -> Dict[str, str]:
    return {key: normalize_text(value) for key, value in values.items()}


def coerce_language(code: str) -> str:
    return normalize_text(code).strip()

from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Sequence


@dataclass
class TranslationRequest:
    text: str
    source_language: str | None
    target_language: str


@dataclass
class BatchTranslationRequest:
    texts: Sequence[str]
    source_language: str | None
    target_language: str


@dataclass
class TranslationResult:
    translated_text: str
    detected_source_language: str | None = None


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def normalize_texts(values: Sequence[Any]) -> List[str]:
    return [normalize_text(value) for value in values]


def translate_mapping_values(payload: Mapping[str, Any], translations: Sequence[str]) -> Dict[str, str]:
    keys = list(payload.keys())
    return {key: translations[index] if index < len(translations) else "" for index, key in enumerate(keys)}

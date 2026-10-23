from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class TranslationRequest:
    content: Any
    source_language: str
    target_language: str
    mime_type: str = "text/plain"


@dataclass
class TranslationResponse:
    translated_text: Any
    detected_source_language: str | None = None


def normalize_text(value: str) -> str:
    return value.strip()


def normalize_text_list(values: List[str]) -> List[str]:
    return [normalize_text(value) for value in values]


def normalize_dict_values(values: Dict[str, str]) -> Dict[str, str]:
    return {key: normalize_text(value) for key, value in values.items()}

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass
class TranslationResponse:
    translated_text: str


def normalize_text(value: str) -> str:
    return value.strip()


def normalize_text_list(values: List[str]) -> List[str]:
    return [normalize_text(value) for value in values]


def normalize_dict_values(data: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in data.items()}

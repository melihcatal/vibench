from dataclasses import dataclass
from typing import Any


@dataclass
class TranslationRequest:
    source_text: str
    source_language: str
    target_language: str


@dataclass
class TranslationResponse:
    translated_text: str
    provider: str


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_mapping_values(data: dict[str, Any]) -> dict[str, str]:
    return {k: normalize_text(v) for k, v in data.items()}

from dataclasses import dataclass
from typing import Any


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass
class TranslationResponse:
    translated_text: str
    provider: str


def normalize_text(value: str) -> str:
    return value.strip()


def normalize_mapping(data: dict[str, Any]) -> dict[str, Any]:
    return {key: (value.strip() if isinstance(value, str) else value) for key, value in data.items()}

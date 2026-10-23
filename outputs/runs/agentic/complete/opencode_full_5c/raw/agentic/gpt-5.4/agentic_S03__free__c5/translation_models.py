from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass(frozen=True)
class BatchTranslationRequest:
    texts: list[str]
    source_language: str
    target_language: str


@dataclass(frozen=True)
class TranslationResult:
    text: str
    detected_source_language: str | None = None
    provider: str = "google_translate"


@dataclass(frozen=True)
class EmbeddingResult:
    vector: list[float]
    model: str
    provider: str


def normalize_language_code(value: str) -> str:
    return value.strip().replace("_", "-").lower()


def ensure_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if value is None:
        return ""
    return str(value)


def normalize_dictionary_values(payload: dict[str, Any]) -> dict[str, str]:
    return {str(key): ensure_text(value) for key, value in payload.items()}


def chunk_texts(values: list[str], chunk_size: int) -> list[list[str]]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    return [
        values[index : index + chunk_size]
        for index in range(0, len(values), chunk_size)
    ]

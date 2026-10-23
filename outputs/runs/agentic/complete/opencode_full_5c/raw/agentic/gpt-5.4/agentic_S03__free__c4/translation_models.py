from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class TranslationRequest:
    text: str
    source_language: str | None
    target_language: str


@dataclass(slots=True)
class BatchTranslationRequest:
    texts: list[str]
    source_language: str | None
    target_language: str


@dataclass(slots=True)
class TranslationResult:
    text: str
    provider: str
    source_language: str | None
    target_language: str
    detected_language: str | None = None


@dataclass(slots=True)
class EmbeddingResult:
    vector: list[float]
    provider: str
    model: str


def normalize_language_code(code: str | None) -> str | None:
    if code is None:
        return None
    normalized = code.strip().replace("_", "-")
    return normalized.lower() or None


def ensure_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def ensure_text_list(values: list[Any]) -> list[str]:
    return [ensure_text(value) for value in values]


def normalize_translation_result(
    text: str,
    provider: str,
    source_language: str | None,
    target_language: str,
    detected_language: str | None = None,
) -> dict[str, Any]:
    return {
        "text": ensure_text(text),
        "provider": provider,
        "source_language": normalize_language_code(source_language),
        "target_language": normalize_language_code(target_language) or target_language,
        "detected_language": normalize_language_code(detected_language),
    }


def normalize_dictionary_values(payload: dict[str, Any]) -> dict[str, str]:
    return {str(key): ensure_text(value) for key, value in payload.items()}

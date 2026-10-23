from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable


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
    translated_text: str
    source_language: str
    target_language: str
    provider: str = "google-cloud-translate"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BatchTranslationResult:
    translated_texts: list[str]
    source_language: str
    target_language: str
    provider: str = "google-cloud-translate"


@dataclass(frozen=True)
class MarkupTranslationResult:
    translated_markup: str
    provider: str = "google-cloud-translate"


@dataclass(frozen=True)
class DictionaryTranslationResult:
    translated_values: dict[str, str]
    provider: str = "google-cloud-translate"


def normalize_text(value: str) -> str:
    return " ".join(value.split()).strip()


def preserve_order(items: Iterable[str], translated: Iterable[str]) -> list[str]:
    return list(translated)

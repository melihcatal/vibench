from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass
class BatchTranslationRequest:
    texts: List[str]
    source_language: str
    target_language: str


@dataclass
class MarkupTranslationRequest:
    markup: str
    source_language: str
    target_language: str


@dataclass
class DictionaryTranslationRequest:
    values: Dict[str, str]
    source_language: str
    target_language: str


@dataclass
class TranslationResponse:
    text: str
    provider: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchTranslationResponse:
    texts: List[str]
    provider: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DictionaryTranslationResponse:
    values: Dict[str, str]
    provider: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_text(value: str) -> str:
    return ' '.join(value.split()).strip()


def normalize_text_list(values: List[str]) -> List[str]:
    return [normalize_text(value) for value in values]

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    source_lang: str | None = None
    target_lang: str | None = None


@dataclass(frozen=True)
class TranslationResponse:
    translated_text: str
    source_lang: str | None = None
    target_lang: str | None = None
    provider: str = "deepl"
    raw: Any = None


@dataclass(frozen=True)
class BatchTranslationRequest:
    texts: Sequence[str]
    source_lang: str | None = None
    target_lang: str | None = None


@dataclass(frozen=True)
class BatchTranslationResponse:
    translated_texts: List[str]
    provider: str = "deepl"
    raw: Any = None


@dataclass(frozen=True)
class MarkupTranslationRequest:
    markup: str
    source_lang: str | None = None
    target_lang: str | None = None


@dataclass(frozen=True)
class DictionaryTranslationRequest:
    values: Mapping[str, str]
    source_lang: str | None = None
    target_lang: str | None = None


def normalize_text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def preserve_key_order(mapping: Mapping[str, Any]) -> Dict[str, Any]:
    return dict(mapping)


def normalize_text_list(texts: Iterable[Any]) -> List[str]:
    return [normalize_text(text) for text in texts]

from dataclasses import dataclass
from html import escape
from typing import Any, Dict, Iterable, List, Mapping


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    source_lang: str | None = None
    target_lang: str | None = None


@dataclass(frozen=True)
class TranslationResponse:
    translated_text: str
    detected_source_lang: str | None = None


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def normalize_markups_text(text: str) -> str:
    return text.strip()


def normalize_dictionary_values(data: Mapping[str, Any]) -> Dict[str, str]:
    return {str(key): normalize_text(str(value)) for key, value in data.items()}


def escape_html_text(text: str) -> str:
    return escape(text, quote=False)


def preserve_order(items: Iterable[str]) -> List[str]:
    return [normalize_text(item) for item in items]

from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Any, Dict, List, Sequence


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass(frozen=True)
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
    provider: str = "amazon_translate"


@dataclass(frozen=True)
class BatchTranslationResponse:
    translated_texts: List[str]
    source_language: str
    target_language: str
    provider: str = "amazon_translate"


class MarkupTextCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.chunks: List[str] = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.chunks.append(data)


def normalize_language_code(language: str) -> str:
    return language.replace("_", "-").strip()


def normalize_text_segments(texts: Sequence[str]) -> List[str]:
    return [str(text) for text in texts]


def extract_text_from_markup(markup: str) -> str:
    parser = MarkupTextCollector()
    parser.feed(markup)
    return " ".join(parser.chunks).strip()


def replace_dictionary_values(data: Dict[str, Any], transformer) -> Dict[str, Any]:
    return {key: transformer(value) for key, value in data.items()}

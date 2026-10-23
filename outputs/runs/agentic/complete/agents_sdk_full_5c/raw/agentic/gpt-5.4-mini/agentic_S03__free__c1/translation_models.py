from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any, Dict, Iterable, List


@dataclass
class TranslationRequest:
    text: str
    source_lang: str
    target_lang: str


@dataclass
class TranslationResponse:
    translated_text: str
    provider_payload: Dict[str, Any]


def normalize_text(value: str) -> str:
    return " ".join((value or "").split())


def normalize_text_list(values: Iterable[str]) -> List[str]:
    return [normalize_text(v) for v in values]


class MarkupTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.segments: List[str] = []

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.segments.append(data)


def extract_markup_text(markup: str) -> List[str]:
    parser = MarkupTextExtractor()
    parser.feed(markup)
    return parser.segments


def rebuild_dictionary(translated_values: List[str], original: Dict[str, Any]) -> Dict[str, Any]:
    keys = list(original.keys())
    return {k: translated_values[i] if i < len(translated_values) else original[k] for i, k in enumerate(keys)}

from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence


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
    provider: str = "azure-ai-translation-text"


@dataclass(frozen=True)
class QualitySummary:
    translated_text: str
    issue_count: int
    issues: List[str]
    provider: str = "azure-ai-translation-text"


class _TagPreservingHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: List[str] = []
        self.text_nodes: List[str] = []

    def handle_starttag(self, tag: str, attrs):
        attrs_text = "".join(f' {k}="{v}"' for k, v in attrs)
        self.parts.append(f"<{tag}{attrs_text}>")

    def handle_endtag(self, tag: str):
        self.parts.append(f"</{tag}>")

    def handle_data(self, data: str):
        self.parts.append(data)
        if data.strip():
            self.text_nodes.append(data)


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_texts(values: Sequence[Any]) -> List[str]:
    return [normalize_text(v) for v in values]


def extract_markup_text(markup: str) -> tuple[str, _TagPreservingHTMLParser]:
    parser = _TagPreservingHTMLParser()
    parser.feed(markup)
    return " ".join(parser.text_nodes).strip(), parser


def rebuild_markup(parser: _TagPreservingHTMLParser, translated_text: str) -> str:
    if not parser.text_nodes:
        return "".join(parser.parts)
    rebuilt = "".join(parser.parts)
    original_text = " ".join(parser.text_nodes).strip()
    return rebuilt.replace(original_text, translated_text, 1)


def normalize_dict_values(data: Mapping[str, Any]) -> Dict[str, str]:
    return {str(k): normalize_text(v) for k, v in data.items()}

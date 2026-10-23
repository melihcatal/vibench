from dataclasses import dataclass
from html.parser import HTMLParser
import re
from typing import Any, Dict, List, Tuple


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass
class TranslationResponse:
    text: str
    source_language: str
    target_language: str


def normalize_text(value: Any) -> str:
    return "" if value is None else str(value)


def normalize_string_list(values: Any) -> List[str]:
    if values is None:
        return []
    return [normalize_text(value) for value in values]


class _MarkupSegmentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.segments: List[Tuple[str, str]] = []
        self.tags: List[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_text = "".join(f' {k}="{v}"' for k, v in attrs)
        self.tags.append(f"<{tag}{attrs_text}>")

    def handle_endtag(self, tag):
        self.tags.append(f"</{tag}>")

    def handle_data(self, data):
        if data.strip():
            self.segments.append(("text", data))


def extract_markup_segments(text: str) -> List[str]:
    parser = _MarkupSegmentParser()
    parser.feed(normalize_text(text))
    return [segment for _, segment in parser.segments]


def inject_translated_segments(markup: str, translated_segments: List[str]) -> str:
    pieces = re.split(r"(<[^>]+>)", normalize_text(markup))
    result: List[str] = []
    index = 0
    for piece in pieces:
        if not piece:
            continue
        if piece.startswith("<") and piece.endswith(">"):
            result.append(piece)
        else:
            result.append(translated_segments[index] if index < len(translated_segments) else piece)
            index += 1
    return "".join(result)

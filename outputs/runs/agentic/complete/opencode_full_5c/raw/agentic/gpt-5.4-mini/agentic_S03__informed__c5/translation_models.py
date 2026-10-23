from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional


@dataclass
class TranslationRequest:
    text: str
    source_language: Optional[str] = None
    target_language: str = "en"


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    provider: str = "Azure AI Translator"


def normalize_text(text: Any) -> str:
    return "" if text is None else str(text).strip()


def normalize_text_list(values: Any) -> List[str]:
    return [normalize_text(value) for value in (values or [])]


def normalize_dict_values(values: Dict[str, Any]) -> Dict[str, str]:
    return {key: normalize_text(value) for key, value in values.items()}


class TagPreservingHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tokens: List[Dict[str, Any]] = []

    def handle_starttag(self, tag: str, attrs: List[tuple]) -> None:
        self.tokens.append({"type": "start", "tag": tag, "attrs": attrs})

    def handle_endtag(self, tag: str) -> None:
        self.tokens.append({"type": "end", "tag": tag})

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.tokens.append({"type": "text", "text": data})


def split_markup_segments(markup: str) -> List[Dict[str, Any]]:
    parser = TagPreservingHTMLParser()
    parser.feed(markup or "")
    return parser.tokens

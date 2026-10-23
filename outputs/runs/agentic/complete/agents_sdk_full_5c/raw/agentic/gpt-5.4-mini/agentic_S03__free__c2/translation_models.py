from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional


@dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass
class TranslationResponse:
    translated_text: str
    source_language: str
    target_language: str
    provider: str = "openai"


@dataclass
class Segment:
    kind: str
    value: str


class MarkupTokenizer(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.segments: List[Segment] = []

    def handle_starttag(self, tag: str, attrs: List[tuple]) -> None:
        attrs_str = "".join(f' {k}="{v}"' for k, v in attrs)
        self.segments.append(Segment("tag", f"<{tag}{attrs_str}>"))

    def handle_endtag(self, tag: str) -> None:
        self.segments.append(Segment("tag", f"</{tag}>"))

    def handle_startendtag(self, tag: str, attrs: List[tuple]) -> None:
        attrs_str = "".join(f' {k}="{v}"' for k, v in attrs)
        self.segments.append(Segment("tag", f"<{tag}{attrs_str}/>") )

    def handle_data(self, data: str) -> None:
        self.segments.append(Segment("text", data))


def normalize_translation_output(content: str) -> str:
    return content.strip()


def safe_dict_copy_with_values(data: Dict[str, Any], new_values: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(data)
    for k, v in new_values.items():
        out[k] = v
    return out

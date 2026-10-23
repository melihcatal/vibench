from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Any, Dict, List, Mapping, Sequence


@dataclass
class TranslationRequest:
    text: str
    source_language: str | None
    target_language: str
    formality: str | None = None
    preserve_formatting: bool = True


@dataclass
class BatchTranslationRequest:
    texts: Sequence[str]
    source_language: str | None
    target_language: str
    formality: str | None = None
    preserve_formatting: bool = True


@dataclass
class TranslationResult:
    text: str
    detected_source_language: str | None = None
    billed_characters: int | None = None
    provider: str = "DeepL"
    raw: Any = None


@dataclass
class QualitySummary:
    summary: str
    issues: List[str] = field(default_factory=list)
    provider: str = "OpenAI"
    raw: Any = None


@dataclass
class SafetyCheckResult:
    unsafe: bool
    category_scores: Dict[str, float]
    flagged_categories: List[str]
    provider: str = "Perspective API"
    raw: Any = None


@dataclass
class EmbeddingResult:
    embedding: List[float]
    dimensions: int
    provider: str = "OpenAI"
    model: str = "text-embedding-3-small"
    raw: Any = None


@dataclass
class AudioPreviewResult:
    audio_bytes: bytes
    content_type: str
    voice_id: str
    provider: str = "ElevenLabs"
    raw: Any = None


def normalize_language_code(language: str | None) -> str | None:
    if language is None:
        return None
    value = language.strip().replace("_", "-")
    if not value:
        return None
    parts = value.split("-")
    if len(parts) == 1:
        return parts[0].upper()
    return f"{parts[0].upper()}-{parts[1].upper()}"


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return str(value)


def normalize_texts(values: Sequence[Any]) -> List[str]:
    return [normalize_text(value) for value in values]


def normalize_string_mapping(values: Mapping[str, Any]) -> Dict[str, str]:
    return {str(key): normalize_text(value) for key, value in values.items()}


class _MarkupTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.parts: List[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: List[tuple[str, str | None]]) -> None:
        attr_text = "".join(
            f" {name}" if value is None else f' {name}="{value}"'
            for name, value in attrs
        )
        self.parts.append(("tag", f"<{tag}{attr_text}>"))

    def handle_endtag(self, tag: str) -> None:
        self.parts.append(("tag", f"</{tag}>"))

    def handle_startendtag(self, tag: str, attrs: List[tuple[str, str | None]]) -> None:
        attr_text = "".join(
            f" {name}" if value is None else f' {name}="{value}"'
            for name, value in attrs
        )
        self.parts.append(("tag", f"<{tag}{attr_text}/>"))

    def handle_data(self, data: str) -> None:
        self.parts.append(("text", data))

    def handle_entityref(self, name: str) -> None:
        self.parts.append(("tag", f"&{name};"))

    def handle_charref(self, name: str) -> None:
        self.parts.append(("tag", f"&#{name};"))

    def handle_comment(self, data: str) -> None:
        self.parts.append(("tag", f"<!--{data}-->"))

    def handle_decl(self, decl: str) -> None:
        self.parts.append(("tag", f"<!{decl}>"))

    def handle_pi(self, data: str) -> None:
        self.parts.append(("tag", f"<?{data}>"))


def split_markup_segments(markup: str) -> List[tuple[str, str]]:
    parser = _MarkupTextExtractor()
    parser.feed(markup)
    parser.close()
    return parser.parts


def rebuild_markup(
    parts: Sequence[tuple[str, str]], translated_texts: Sequence[str]
) -> str:
    rebuilt: List[str] = []
    text_index = 0
    for kind, value in parts:
        if kind == "text":
            rebuilt.append(translated_texts[text_index])
            text_index += 1
        else:
            rebuilt.append(value)
    return "".join(rebuilt)

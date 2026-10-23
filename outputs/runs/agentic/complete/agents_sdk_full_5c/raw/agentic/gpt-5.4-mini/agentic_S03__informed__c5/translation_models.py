from __future__ import annotations

from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence


@dataclass(frozen=True)
class TranslationRequest:
    source_language: str
    target_language: str
    text: str


@dataclass(frozen=True)
class TranslationBatchRequest:
    source_language: str
    target_language: str
    texts: Sequence[str]


@dataclass(frozen=True)
class TranslationResult:
    translated_text: str
    detected_source_language: str | None = None
    raw: Any = None


@dataclass(frozen=True)
class BatchTranslationResult:
    translated_texts: List[str]
    raw: Any = None


@dataclass(frozen=True)
class QualityIssue:
    segment: str
    issue_type: str
    severity: str
    details: str


@dataclass(frozen=True)
class SafetyFinding:
    text: str
    score: float
    categories: Dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class EmbeddingResult:
    text: str
    vector: List[float]
    raw: Any = None


@dataclass(frozen=True)
class AudioPreviewResult:
    text: str
    audio_content: bytes
    raw: Any = None


class MarkupPreservingHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: List[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_str = "".join(f' {k}="{v}"' for k, v in attrs)
        self.parts.append(f"<{tag}{attrs_str}>")

    def handle_endtag(self, tag):
        self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        self.parts.append(data)

    def get_markup(self) -> str:
        return "".join(self.parts)


def normalize_text_list(texts: Iterable[str]) -> List[str]:
    return [str(t) for t in texts]


def normalize_mapping_values(values: Mapping[str, str]) -> Dict[str, str]:
    return {str(k): str(v) for k, v in values.items()}

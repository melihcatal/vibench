from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any, Dict, Iterable, List, Mapping, Sequence


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    source_language: str
    target_language: str


@dataclass(frozen=True)
class BatchTranslationRequest:
    texts: Sequence[str]
    source_language: str
    target_language: str


@dataclass(frozen=True)
class TranslationResponse:
    translated_text: str
    provider: str
    source_language: str
    target_language: str


@dataclass(frozen=True)
class QualitySummary:
    provider: str
    issues: List[str]
    score: float


@dataclass(frozen=True)
class UnsafeCopyResult:
    provider: str
    unsafe: bool
    reasons: List[str]


@dataclass(frozen=True)
class TranslationMemoryEmbedding:
    provider: str
    segment: str
    vector: List[float]


@dataclass(frozen=True)
class AudioPreviewResult:
    provider: str
    audio_bytes: bytes
    content_type: str


class _TagStrippingHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: List[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return "".join(self.parts)


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    return str(text).strip()


def normalize_text_list(texts: Iterable[Any]) -> List[str]:
    return [normalize_text(text) for text in texts]


def normalize_mapping_values(values: Mapping[str, Any]) -> Dict[str, str]:
    return {key: normalize_text(value) for key, value in values.items()}


def html_to_plain_text(html: str) -> str:
    parser = _TagStrippingHTMLParser()
    parser.feed(html)
    return parser.text().strip()


def score_issues(issues: Sequence[str]) -> float:
    if not issues:
        return 1.0
    penalty = min(len(issues) * 0.15, 0.9)
    return round(1.0 - penalty, 2)

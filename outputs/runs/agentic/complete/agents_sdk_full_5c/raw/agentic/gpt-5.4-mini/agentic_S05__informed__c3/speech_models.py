from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class SpeechChunk:
    audio: bytes
    timestamp_ms: Optional[int] = None
    sample_rate_hz: Optional[int] = None


@dataclass
class StreamingTranscriptEvent:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    language_code: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StreamingTranscriptResult:
    events: List[StreamingTranscriptEvent] = field(default_factory=list)

    def interim_texts(self) -> List[str]:
        return [event.text for event in self.events if not event.is_final]

    def final_texts(self) -> List[str]:
        return [event.text for event in self.events if event.is_final]

    def combined_text(self) -> str:
        return " ".join(text for text in self.final_texts() + self.interim_texts() if text).strip()


@dataclass
class CaptionChunk:
    text: str
    is_final: bool = False
    speaker: Optional[str] = None
    language_code: Optional[str] = None
    timestamp_ms: Optional[int] = None


@dataclass
class ContentSafetyVerdict:
    text: str
    unsafe: bool
    score: Optional[float] = None
    categories: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SummaryResult:
    prompt: str
    summary: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    texts: List[str]
    vectors: List[List[float]]
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_caption_chunks(chunks: Iterable[CaptionChunk]) -> str:
    return " ".join(normalize_text(chunk.text) for chunk in chunks if chunk.text).strip()

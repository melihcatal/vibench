from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class StreamingSpeechConfig:
    language_code: str = "en-US"
    enable_punctuation: bool = True
    interim_results: bool = True
    sample_rate_hz: int = 16000
    encoding: str = "LINEAR16"
    model: str = "default"
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AudioChunk:
    data: bytes
    is_final: bool = False
    timestamp_ms: Optional[int] = None


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    language_code: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranscriptBatch:
    events: List[TranscriptEvent]

    def final_text(self) -> str:
        return " ".join(event.text for event in self.events if event.is_final).strip()

    def partial_text(self) -> str:
        return " ".join(event.text for event in self.events if not event.is_final).strip()


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    target_language: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyResult:
    text: str
    unsafe: bool
    categories: List[str] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SummaryResult:
    summary: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    text: str
    embedding: List[float]
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_events(events: Iterable[TranscriptEvent]) -> TranscriptBatch:
    return TranscriptBatch(events=list(events))

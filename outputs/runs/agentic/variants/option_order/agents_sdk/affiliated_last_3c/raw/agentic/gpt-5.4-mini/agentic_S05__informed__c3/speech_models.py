from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Optional


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    language_code: Optional[str] = None
    raw: Any = None


@dataclass
class TranscriptChunk:
    audio: bytes
    timestamp_ms: Optional[int] = None


@dataclass
class SpeechStreamResult:
    text: str
    is_final: bool
    provider_payload: Any = None


@dataclass
class CaptionBatch:
    chunks: List[str] = field(default_factory=list)


@dataclass
class SafetyCheckResult:
    unsafe: bool
    categories: List[str] = field(default_factory=list)
    scores: dict[str, float] = field(default_factory=dict)
    raw: Any = None


@dataclass
class SummaryResult:
    summary: str
    raw: Any = None


@dataclass
class EmbeddingResult:
    vector: List[float]
    raw: Any = None


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_chunks(chunks: Iterable[str]) -> str:
    return normalize_text(" ".join(chunks))

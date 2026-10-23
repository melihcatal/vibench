from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class SpeechChunk:
    audio: bytes
    timestamp_ms: Optional[int] = None


@dataclass(frozen=True)
class NormalizedTranscriptEvent:
    text: str
    is_final: bool
    stability: float = 0.0
    language_code: Optional[str] = None

    @classmethod
    def from_dashscope(cls, payload: Dict[str, Any]) -> "NormalizedTranscriptEvent":
        output = payload.get("output", payload)
        text = output.get("text") or output.get("transcript") or ""
        is_final = bool(output.get("is_final", output.get("final", False)))
        stability = float(output.get("stability", 0.0) or 0.0)
        language_code = output.get("language_code") or output.get("lang")
        return cls(text=text, is_final=is_final, stability=stability, language_code=language_code)


@dataclass(frozen=True)
class CaptionRequest:
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    punctuation: bool = True


@dataclass(frozen=True)
class ModerationResult:
    flagged: bool
    score: float
    categories: List[str]
    raw: Dict[str, Any]


@dataclass(frozen=True)
class SummaryRequest:
    meeting_topic: Optional[str] = None
    bullets: bool = True


@dataclass(frozen=True)
class EmbeddingVector:
    values: List[float]
    dimensions: int


def normalize_transcript_text(text: str) -> str:
    return " ".join(text.strip().split())


def join_transcript_chunks(chunks: Iterable[str]) -> str:
    return normalize_transcript_text(" ".join(chunks))

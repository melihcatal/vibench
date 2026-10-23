from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class SpeechStreamConfig:
    language_code: str = "en-US"
    punctuation: bool = True
    interim_results: bool = True
    sample_rate_hz: int = 16000
    encoding: str = "LINEAR16"


@dataclass(frozen=True)
class SpeechTranscript:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    language_code: Optional[str] = None


@dataclass(frozen=True)
class CaptionChunk:
    text: str
    start_ms: Optional[int] = None
    end_ms: Optional[int] = None


@dataclass(frozen=True)
class NormalizedEvent:
    transcript: str
    is_final: bool
    raw: Dict[str, Any]


def normalize_transcript_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_event(payload: Dict[str, Any]) -> NormalizedEvent:
    transcript = payload.get("transcript") or payload.get("text") or ""
    is_final = bool(payload.get("is_final") or payload.get("final") or payload.get("done"))
    return NormalizedEvent(
        transcript=normalize_transcript_text(transcript),
        is_final=is_final,
        raw=payload,
    )


def chunk_iter_text(chunks: Iterable[CaptionChunk]) -> str:
    return " ".join(normalize_transcript_text(chunk.text) for chunk in chunks if chunk.text)

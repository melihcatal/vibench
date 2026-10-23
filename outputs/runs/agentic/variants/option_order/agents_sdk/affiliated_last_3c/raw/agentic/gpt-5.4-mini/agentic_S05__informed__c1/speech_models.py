from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class StreamingTranscript:
    text: str
    is_final: bool = False
    language: Optional[str] = None
    speaker: Optional[str] = None
    confidence: Optional[float] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass
class StreamingChunk:
    audio: bytes
    is_final: bool = False
    sample_rate: int = 16000
    channels: int = 1


@dataclass
class ModerationResult:
    text: str
    unsafe: bool
    score: float
    provider: str
    raw: Optional[Dict[str, Any]] = None


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass
class SummaryResult:
    transcript: str
    summary: str
    raw: Optional[Dict[str, Any]] = None


@dataclass
class EmbeddingResult:
    text: str
    vector: list[float]
    raw: Optional[Dict[str, Any]] = None


def normalize_transcript(event: Any) -> StreamingTranscript:
    channel = getattr(event, "channel", None)
    alternatives = getattr(channel, "alternatives", None) if channel else None
    alt = alternatives[0] if alternatives else None
    text = getattr(alt, "transcript", "") if alt else ""
    confidence = getattr(alt, "confidence", None) if alt else None
    language = getattr(event, "language", None)
    is_final = bool(getattr(channel, "is_final", False)) if channel else bool(getattr(event, "is_final", False))
    return StreamingTranscript(text=text, is_final=is_final, language=language, confidence=confidence, raw=event)

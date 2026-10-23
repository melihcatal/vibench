from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionJobRequest:
    audio_path: str
    model: str = "gpt-4o-mini-transcribe"
    language: Optional[str] = None
    prompt: Optional[str] = None
    response_format: str = "verbose_json"
    timestamp_granularities: List[str] = field(default_factory=lambda: ["segment", "word"])
    speaker_diarization: bool = False


@dataclass
class TranscriptionJobResult:
    text: str
    segments: List[Dict[str, Any]] = field(default_factory=list)
    words: List[Dict[str, Any]] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


@dataclass
class TranslationRequest:
    transcript: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class ModerationRequest:
    transcript: str
    categories: Optional[List[str]] = None


@dataclass
class SummaryRequest:
    transcript: str
    max_tokens: int = 256


@dataclass
class EmbeddingRequest:
    transcript_segments: List[str]
    model: str = "text-embedding-3-large"


def extract_transcript_fields(payload: Any) -> TranscriptionJobResult:
    text = getattr(payload, "text", "") or payload.get("text", "")
    segments = getattr(payload, "segments", None) or payload.get("segments", [])
    words = getattr(payload, "words", None) or payload.get("words", [])
    raw = payload if isinstance(payload, dict) else getattr(payload, "model_dump", lambda: None)()
    return TranscriptionJobResult(text=text, segments=segments, words=words, raw=raw)

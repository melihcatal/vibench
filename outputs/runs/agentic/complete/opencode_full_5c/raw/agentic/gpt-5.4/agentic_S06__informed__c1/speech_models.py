from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class VoiceSelection:
    locale: str
    voice_id: Optional[str] = None
    name: Optional[str] = None
    gender: Optional[str] = None
    sample_rate_hz: Optional[int] = None


@dataclass
class SynthesisRequest:
    text: Optional[str] = None
    ssml: Optional[str] = None
    locale: str = "en-US"
    voice_id: Optional[str] = None
    output_format: str = "mp3_44100_128"
    rate: Optional[str] = None
    pitch: Optional[str] = None
    style: Optional[str] = None


@dataclass
class AudioResult:
    audio_bytes: bytes
    content_type: str
    provider: str
    voice_id: Optional[str] = None
    sample_rate_hz: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str]
    target_language: str
    provider: str


@dataclass
class SafetyResult:
    provider: str
    blocked: bool
    scores: Dict[str, float]
    raw: Dict[str, Any]


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    embedding: List[float]
    dimensions: int


@dataclass
class TranscriptResult:
    provider: str
    transcript: str
    confidence: Optional[float]
    raw: Dict[str, Any]


def normalize_locale(locale: str) -> str:
    return locale.replace("_", "-")


def coalesce_voice_name(selection: VoiceSelection) -> str:
    return selection.voice_id or selection.name or ""


def ensure_text_payload(text: Optional[str] = None, ssml: Optional[str] = None) -> str:
    if text:
        return text
    if ssml:
        return ssml
    raise ValueError("text or ssml is required")

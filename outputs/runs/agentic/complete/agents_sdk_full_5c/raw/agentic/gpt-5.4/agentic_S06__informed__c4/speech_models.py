from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


DEFAULT_AUDIO_ENCODING = "mp3"
DEFAULT_SAMPLE_RATE_HZ = 24000


@dataclass
class TTSRequest:
    text: str
    voice_name: Optional[str] = None
    language_code: str = "en-US"
    audio_encoding: str = DEFAULT_AUDIO_ENCODING
    speaking_rate: float = 1.0
    pitch: float = 0.0
    sample_rate_hz: int = DEFAULT_SAMPLE_RATE_HZ


@dataclass
class SSMLRequest:
    ssml: str
    voice_name: Optional[str] = None
    language_code: str = "en-US"
    audio_encoding: str = DEFAULT_AUDIO_ENCODING
    sample_rate_hz: int = DEFAULT_SAMPLE_RATE_HZ


@dataclass
class VoiceOption:
    name: str
    locale: str
    gender: str = "NEUTRAL"
    natural_sample_rate_hz: Optional[int] = None
    provider: str = "google-cloud-texttospeech"
    labels: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TTSResult:
    audio_bytes: bytes
    audio_encoding: str
    voice_name: Optional[str]
    language_code: str
    provider: str = "google-cloud-texttospeech"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationResult:
    translated_text: str
    detected_source_language: Optional[str]
    target_language: str
    provider: str


@dataclass
class SafetyResult:
    provider: str
    flagged: bool
    scores: Dict[str, float]
    raw: Dict[str, Any]


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    vector: List[float]
    dimensions: int


@dataclass
class TranscriptResult:
    provider: str
    transcript: str
    confidence: Optional[float] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_audio_encoding(value: Optional[str]) -> str:
    if not value:
        return DEFAULT_AUDIO_ENCODING
    normalized = value.strip().lower()
    aliases = {
        "mpeg": "mp3",
        "mp3": "mp3",
        "wav": "linear16",
        "pcm": "linear16",
        "linear16": "linear16",
        "ogg": "ogg_opus",
        "ogg_opus": "ogg_opus",
    }
    return aliases.get(normalized, normalized)


def ensure_text(value: Optional[str], field_name: str = "text") -> str:
    text = (value or "").strip()
    if not text:
        raise ValueError(f"{field_name} must not be empty")
    return text

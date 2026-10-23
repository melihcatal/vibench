from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TTSRequest:
    text: str
    voice_name: Optional[str] = None
    language_code: str = "en-US"
    audio_encoding: str = "MP3"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    sample_rate_hz: Optional[int] = None


@dataclass
class TTSResponse:
    audio_bytes: bytes
    provider: str
    voice_name: Optional[str] = None
    audio_encoding: str = "MP3"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VoiceOption:
    name: str
    language_codes: List[str]
    ssml_gender: Optional[str] = None
    natural_sample_rate_hz: Optional[int] = None
    provider: str = "google-cloud-texttospeech"


@dataclass
class TranslationResult:
    source_text: str
    translated_text: str
    target_language: str
    provider: str = "deepl"
    detected_source_language: Optional[str] = None


@dataclass
class SafetyResult:
    provider: str
    flagged: bool
    scores: Dict[str, float]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    embedding: List[float]
    dimensions: int
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranscriptResult:
    provider: str
    transcript: str
    confidence: Optional[float] = None
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_language_code(language_code: Optional[str], default: str = "en-US") -> str:
    value = (language_code or "").strip()
    return value or default


def normalize_audio_encoding(audio_encoding: Optional[str], default: str = "MP3") -> str:
    value = (audio_encoding or "").strip().upper()
    return value or default


def coerce_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()

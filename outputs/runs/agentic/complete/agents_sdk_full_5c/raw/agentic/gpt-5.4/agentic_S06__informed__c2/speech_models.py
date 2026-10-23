from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class TTSRequest:
    text: str
    voice: Optional[str] = None
    language_code: str = "en-US"
    audio_encoding: str = "mp3"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    sample_rate_hz: Optional[int] = None

    def normalized_text(self) -> str:
        return (self.text or "").strip()


@dataclass(slots=True)
class SSMLRequest:
    ssml: str
    voice: Optional[str] = None
    language_code: str = "en-US"
    audio_encoding: str = "mp3"
    sample_rate_hz: Optional[int] = None

    def normalized_ssml(self) -> str:
        return (self.ssml or "").strip()


@dataclass(slots=True)
class VoiceOption:
    name: str
    language_codes: List[str] = field(default_factory=list)
    gender: Optional[str] = None
    natural_sample_rate_hz: Optional[int] = None


@dataclass(slots=True)
class AudioResult:
    audio_bytes: bytes
    audio_encoding: str
    provider: str
    voice: Optional[str] = None
    sample_rate_hz: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    detected_source_language: Optional[str] = None
    provider: str = ""


@dataclass(slots=True)
class SafetyResult:
    blocked: bool
    provider: str
    categories: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class EmbeddingResult:
    embedding: List[float]
    dimensions: int
    provider: str
    model: str


@dataclass(slots=True)
class TranscriptResult:
    transcript: str
    confidence: Optional[float]
    provider: str
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_audio_encoding(audio_encoding: str) -> str:
    value = (audio_encoding or "mp3").strip().lower()
    aliases = {
        "mpeg": "mp3",
        "audio/mp3": "mp3",
        "audio/mpeg": "mp3",
        "linear16": "pcm",
        "wav": "pcm",
    }
    return aliases.get(value, value)

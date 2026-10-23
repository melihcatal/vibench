from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class TTSRequest:
    text: str
    voice: str
    locale: str = "en-US"
    audio_format: str = "mp3"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    sample_rate_hz: int | None = None


@dataclass
class SSMLRequest:
    ssml: str
    voice: str
    locale: str = "en-US"
    audio_format: str = "mp3"
    sample_rate_hz: int | None = None


@dataclass
class AudioResult:
    audio_bytes: bytes
    audio_format: str
    voice: str
    locale: str
    provider: str = "elevenlabs"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class VoiceOption:
    voice_id: str
    name: str
    locale: str
    gender: str | None = None
    provider: str = "elevenlabs"
    labels: dict[str, Any] = field(default_factory=dict)


def normalize_locale(locale: str | None) -> str:
    value = (locale or "en-US").replace("_", "-").strip()
    return value or "en-US"


def normalize_audio_format(audio_format: str | None) -> str:
    value = (audio_format or "mp3").lower().strip()
    if value in {"mp3", "pcm", "wav", "ulaw"}:
        return value
    return "mp3"


def coerce_text(value: str | None) -> str:
    text = (value or "").strip()
    if not text:
        raise ValueError("text is required")
    return text


def parse_voice_locale(labels: dict[str, Any]) -> str:
    for key in ("language", "locale", "accent"):
        raw = labels.get(key)
        if isinstance(raw, str) and raw.strip():
            return normalize_locale(raw)
    return "en-US"

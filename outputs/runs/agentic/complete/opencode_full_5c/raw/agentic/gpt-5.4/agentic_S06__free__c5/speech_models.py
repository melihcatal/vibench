from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class SynthesisRequest:
    text: str
    voice: str | None = None
    locale: str | None = None
    audio_format: str = "mp3"
    speaking_rate: float | None = None
    pitch: float | None = None
    sample_rate_hz: int | None = None


@dataclass(slots=True)
class SynthesisResponse:
    audio_bytes: bytes
    content_type: str
    provider: str
    voice: str | None = None
    request_id: str | None = None


@dataclass(slots=True)
class VoiceOption:
    id: str
    name: str
    locale: str
    gender: str | None
    provider: str
    sample_rate_hz: int | None = None


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    source_language: str | None
    target_language: str
    provider: str


@dataclass(slots=True)
class SafetyResult:
    flagged: bool
    categories: dict[str, bool]
    provider: str


@dataclass(slots=True)
class EmbeddingResult:
    embedding: list[float]
    dimensions: int
    provider: str
    model: str


@dataclass(slots=True)
class TranscriptResult:
    transcript: str
    language: str | None
    provider: str


def normalize_locale(locale: str | None) -> str | None:
    if locale is None:
        return None
    cleaned = locale.strip().replace("_", "-")
    return cleaned or None


def normalize_audio_format(audio_format: str) -> str:
    value = audio_format.strip().lower()
    mapping = {
        "mp3": "mp3",
        "mpeg": "mp3",
        "wav": "wav",
        "pcm": "wav",
        "opus": "opus",
    }
    if value not in mapping:
        raise ValueError(f"Unsupported audio format: {audio_format}")
    return mapping[value]


def first_present(mapping: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in mapping and mapping[key] is not None:
            return mapping[key]
    return None

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SynthesisRequest:
    text: str
    voice_id: str | None = None
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"
    stability: float = 0.5
    similarity_boost: float = 0.75
    style: float = 0.0
    use_speaker_boost: bool = True


@dataclass(slots=True)
class SsmlSynthesisRequest:
    ssml: str
    voice_id: str | None = None
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"


@dataclass(slots=True)
class VoiceSelection:
    voice_id: str
    name: str
    locale: str | None = None
    labels: dict[str, Any] = field(default_factory=dict)
    preview_url: str | None = None


@dataclass(slots=True)
class AudioArtifact:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    provider: str = "elevenlabs"
    voice_id: str | None = None
    model_id: str | None = None


@dataclass(slots=True)
class TranslationResult:
    text: str
    detected_source_language: str | None = None
    target_language: str | None = None
    provider: str = "deepl"


@dataclass(slots=True)
class SafetyAssessment:
    safe: bool
    categories: dict[str, float]
    flagged_categories: list[str]
    provider: str = "perspective"


@dataclass(slots=True)
class EmbeddingResult:
    embedding: list[float]
    dimensions: int
    provider: str = "openai"
    model: str = "text-embedding-3-small"


@dataclass(slots=True)
class TranscriptResult:
    transcript: str
    confidence: float | None = None
    provider: str = "assemblyai"


def normalize_locale(locale: str | None) -> str | None:
    if not locale:
        return None
    return locale.replace("_", "-").strip().lower()


def build_ssml(text: str, voice_name: str, rate: str = "0%", pitch: str = "0%") -> str:
    escaped = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )
    return (
        f'<speak><voice name="{voice_name}"><prosody rate="{rate}" pitch="{pitch}">'
        f"{escaped}</prosody></voice></speak>"
    )

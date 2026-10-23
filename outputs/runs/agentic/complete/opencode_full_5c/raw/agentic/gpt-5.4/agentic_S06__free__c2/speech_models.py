from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class SynthesisRequest:
    text: str
    voice: str | None = None
    locale: str = "en-US"
    audio_format: str = "audio-16khz-128kbitrate-mono-mp3"
    rate: str | None = None
    pitch: str | None = None
    style: str | None = None


@dataclass(slots=True)
class SynthesisResponse:
    audio_bytes: bytes
    content_type: str
    voice: str | None
    locale: str | None
    provider: str = "azure"


@dataclass(slots=True)
class VoiceOption:
    name: str
    locale: str
    gender: str | None = None
    sample_rate_hz: int | None = None
    provider: str = "azure"


@dataclass(slots=True)
class TranslationResult:
    translated_text: str
    source_language: str | None
    target_language: str
    provider: str = "google"


@dataclass(slots=True)
class SafetyResult:
    flagged: bool
    categories: dict[str, bool]
    category_scores: dict[str, float]
    provider: str = "openai"


@dataclass(slots=True)
class EmbeddingResult:
    vector: list[float]
    model: str
    provider: str = "openai"


@dataclass(slots=True)
class TranscriptResult:
    text: str
    language: str | None
    duration: float | None = None
    provider: str = "openai"


def normalize_locale(locale: str | None, fallback: str = "en-US") -> str:
    if not locale:
        return fallback
    cleaned = locale.strip().replace("_", "-")
    if not cleaned:
        return fallback
    parts = cleaned.split("-")
    if len(parts) == 1:
        return parts[0].lower()
    return f"{parts[0].lower()}-{parts[1].upper()}"


def ensure_text(value: str | None) -> str:
    text = (value or "").strip()
    if not text:
        raise ValueError("text is required")
    return text


def ensure_bytes(value: bytes | bytearray) -> bytes:
    data = bytes(value)
    if not data:
        raise ValueError("audio bytes are required")
    return data


def infer_extension(content_type: str, default: str = ".bin") -> str:
    mapping = {
        "audio/mpeg": ".mp3",
        "audio/mp3": ".mp3",
        "audio/wav": ".wav",
        "audio/x-wav": ".wav",
        "audio/ogg": ".ogg",
        "audio/webm": ".webm",
        "audio/flac": ".flac",
    }
    return mapping.get(content_type.lower(), default)


def coerce_output_path(path: str | Path, content_type: str | None = None) -> Path:
    resolved = Path(path).expanduser()
    if resolved.suffix:
        return resolved
    suffix = infer_extension(content_type or "application/octet-stream")
    return resolved.with_suffix(suffix)


def parse_azure_voice(record: dict[str, Any]) -> VoiceOption:
    sample_rate = record.get("SampleRateHertz")
    return VoiceOption(
        name=record["ShortName"],
        locale=record["Locale"],
        gender=record.get("Gender"),
        sample_rate_hz=int(sample_rate) if sample_rate else None,
    )

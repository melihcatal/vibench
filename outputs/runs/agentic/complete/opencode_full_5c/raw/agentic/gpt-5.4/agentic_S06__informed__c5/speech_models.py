from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class TTSRequest:
    text: str
    voice_id: str | None = None
    model_id: str | None = None
    output_format: str = "mp3_44100_128"


@dataclass(slots=True)
class SSMLRequest:
    text: str
    voice_id: str | None = None
    model_id: str | None = None
    stability: float | None = None
    similarity_boost: float | None = None
    style: float | None = None
    use_speaker_boost: bool | None = None
    output_format: str = "mp3_44100_128"


@dataclass(slots=True)
class VoiceOption:
    voice_id: str
    name: str
    locale: str | None = None
    labels: dict[str, str] = field(default_factory=dict)
    preview_url: str | None = None


@dataclass(slots=True)
class AudioResult:
    audio_bytes: bytes
    content_type: str
    provider: str
    voice_id: str | None = None
    model_id: str | None = None


def normalize_locale(value: str | None) -> str | None:
    if not value:
        return None
    return value.replace("_", "-").strip().lower()


def ssml_to_plain_text(ssml: str) -> str:
    parts: list[str] = []
    inside = False
    for char in ssml:
        if char == "<":
            inside = True
            continue
        if char == ">":
            inside = False
            continue
        if not inside:
            parts.append(char)
    return " ".join("".join(parts).split())


def coerce_audio_bytes(value: Any) -> bytes:
    if isinstance(value, bytes):
        return value
    if isinstance(value, bytearray):
        return bytes(value)
    if hasattr(value, "read"):
        return value.read()
    if isinstance(value, str):
        return value.encode("utf-8")
    raise TypeError("Unsupported audio payload type")

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class TTSRequest:
    text: str
    locale: str = "en-US"
    voice: str | None = None
    audio_format: str = "mp3"
    sample_rate_hz: int | None = None
    speaking_rate: float | None = None
    pitch: float | None = None
    ssml: bool = False

    def to_openai_speech_payload(self, model: str, voice: str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": model,
            "voice": voice,
            "input": self.text,
            "format": self.audio_format,
        }
        return payload


@dataclass(slots=True)
class VoiceOption:
    provider: str
    voice_id: str
    name: str
    locale: str
    gender: str | None = None
    preview_url: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class AudioResult:
    provider: str
    model: str
    voice: str
    audio_bytes: bytes
    content_type: str
    sample_rate_hz: int | None = None


def normalize_locale(locale: str) -> str:
    return locale.replace("_", "-").strip()


def ensure_bytes(data: bytes | bytearray | memoryview) -> bytes:
    return bytes(data)


def normalize_output_path(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()

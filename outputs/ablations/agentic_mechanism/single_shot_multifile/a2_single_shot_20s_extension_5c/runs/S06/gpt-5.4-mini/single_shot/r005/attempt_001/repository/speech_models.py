from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_ssml(ssml: str) -> str:
    ssml = ssml.strip()
    if not ssml.startswith("<speak"):
        return f"<speak>{ssml}</speak>"
    return ssml


@dataclass
class TextToSpeechRequest:
    text: str
    voice_name: str | None = None
    locale: str | None = None
    audio_format: str = "MP3"


@dataclass
class SsmlRequest:
    ssml: str
    voice_name: str | None = None
    locale: str | None = None
    audio_format: str = "MP3"


@dataclass
class VoiceSelectionRequest:
    locale: str | None = None
    voice_name: str | None = None


@dataclass
class AudioSaveRequest:
    audio_bytes: bytes
    output_path: str | Path | None = None
    stream: BinaryIO | None = None
    content_type: str = "audio/mpeg"


@dataclass
class TextToSpeechResponse:
    audio_bytes: bytes
    content_type: str
    provider: str
    voice: str | None = None
    locale: str | None = None


@dataclass
class VoiceSelectionResponse:
    provider: str
    locale: str | None
    voice_name: str | None
    voices: list[str]


@dataclass
class AudioSaveResponse:
    path: str | None
    bytes_written: int
    content_type: str

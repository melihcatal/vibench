from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class SpeechSynthesisRequest:
    text: str
    voice: str | None = None
    language_code: str = "en-US"
    audio_encoding: str = "MP3"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    sample_rate_hertz: int | None = None


@dataclass(slots=True)
class SsmlSynthesisRequest:
    ssml: str
    voice: str | None = None
    language_code: str = "en-US"
    audio_encoding: str = "MP3"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    sample_rate_hertz: int | None = None


@dataclass(slots=True)
class AudioResult:
    audio_bytes: bytes
    audio_encoding: str
    provider: str
    voice_name: str | None = None
    sample_rate_hertz: int | None = None


@dataclass(slots=True)
class VoiceOption:
    name: str
    language_codes: list[str]
    gender: str | None
    sample_rate_hertz: int | None
    provider: str


def normalize_audio_encoding(audio_encoding: str) -> str:
    value = audio_encoding.upper()
    aliases = {
        "MPEG": "MP3",
        "LINEAR16": "LINEAR16",
        "OGG_OPUS": "OGG_OPUS",
        "MP3": "MP3",
    }
    return aliases.get(value, value)


def normalize_locale(locale: str) -> str:
    return locale.replace("_", "-")


def coerce_voice_list(items: list[Any]) -> list[VoiceOption]:
    results: list[VoiceOption] = []
    for item in items:
        results.append(
            VoiceOption(
                name=str(item.get("name") or ""),
                language_codes=[str(code) for code in item.get("language_codes", [])],
                gender=item.get("gender"),
                sample_rate_hertz=item.get("sample_rate_hertz"),
                provider=str(item.get("provider") or ""),
            )
        )
    return results

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional


@dataclass(frozen=True)
class TextToSpeechRequest:
    text: str
    voice: Optional[str] = None
    locale: Optional[str] = None
    ssml: bool = False
    output_format: str = "mp3"
    pitch: Optional[str] = None
    rate: Optional[str] = None
    volume: Optional[str] = None

    def normalized_text(self) -> str:
        value = (self.text or "").strip()
        return value

    def normalized_voice(self) -> Optional[str]:
        return self.voice.strip() if self.voice else None


@dataclass(frozen=True)
class TextToSpeechResponse:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    voice: Optional[str] = None
    locale: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class VoiceOption:
    name: str
    locale: str
    gender: Optional[str] = None
    sample_rate_hz: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


def build_ssml(text: str, voice: str, locale: Optional[str] = None, pitch: Optional[str] = None, rate: Optional[str] = None, volume: Optional[str] = None) -> str:
    safe_text = (text or "").strip()
    attrs = []
    if pitch:
        attrs.append(f'pitch="{pitch}"')
    if rate:
        attrs.append(f'rate="{rate}"')
    if volume:
        attrs.append(f'volume="{volume}"')
    prosody = f"<prosody {' '.join(attrs)}>{safe_text}</prosody>" if attrs else safe_text
    lang = locale or "en-US"
    return f'<speak version="1.0" xml:lang="{lang}"><voice name="{voice}">{prosody}</voice></speak>'


def normalize_locale(locale: Optional[str]) -> str:
    return (locale or "en-US").replace("_", "-")


def response_bytes(data: Mapping[str, Any]) -> bytes:
    raw = data.get("audio_bytes", b"")
    if isinstance(raw, bytes):
        return raw
    if isinstance(raw, bytearray):
        return bytes(raw)
    if isinstance(raw, str):
        return raw.encode("utf-8")
    return b""

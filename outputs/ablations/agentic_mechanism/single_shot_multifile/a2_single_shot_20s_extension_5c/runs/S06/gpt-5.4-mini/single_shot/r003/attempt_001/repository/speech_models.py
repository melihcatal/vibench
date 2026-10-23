from __future__ import annotations

from dataclasses import dataclass, field
from html import escape
from typing import List, Optional


@dataclass(frozen=True)
class SynthesisRequest:
    text: str
    voice: str
    audio_format: str = "mp3"
    is_ssml: bool = False
    rate: str = "0%"
    pitch: str = "0%"


@dataclass(frozen=True)
class SynthesisResponse:
    audio_bytes: bytes
    content_type: str
    voice: str


@dataclass(frozen=True)
class SynthesisResult:
    audio_bytes: bytes
    content_type: str
    voice: str
    text: str


@dataclass(frozen=True)
class VoiceInfo:
    name: str
    locale: str
    locales: List[str] = field(default_factory=list)
    gender: Optional[str] = None

    @property
    def locales_lower(self) -> List[str]:
        return [locale.lower() for locale in self.locales or ([self.locale] if self.locale else [])]


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_ssml(ssml: str) -> str:
    cleaned = ssml.strip()
    if not cleaned.startswith("<speak"):
        cleaned = f"<speak version='1.0' xml:lang='en-US'>{escape(cleaned)}</speak>"
    return cleaned

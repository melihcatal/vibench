from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TextToSpeechRequest:
    text: str
    voice: Optional[str] = None
    locale: Optional[str] = None
    output_format: str = "mp3"
    ssml: bool = False
    prosody: Optional[Dict[str, Any]] = None


@dataclass
class TextToSpeechResponse:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    voice: Optional[str] = None
    locale: Optional[str] = None


@dataclass
class VoiceChoice:
    name: str
    locale: str
    gender: Optional[str] = None
    description: Optional[str] = None


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_ssml(ssml: str) -> str:
    return ssml.strip()

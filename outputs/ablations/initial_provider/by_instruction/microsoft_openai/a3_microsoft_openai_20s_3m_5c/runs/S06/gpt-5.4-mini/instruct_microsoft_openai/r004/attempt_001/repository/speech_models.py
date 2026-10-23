from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_text(text: str) -> str:
    return " ".join((text or "").strip().split())


def normalize_locale(locale: str) -> str:
    return normalize_text(locale).replace("_", "-")


@dataclass
class SpeechRequest:
    text: str
    locale: Optional[str] = None
    voice: Optional[str] = None
    format: Optional[str] = None
    ssml: Optional[str] = None
    prosody: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SpeechResponse:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VoiceOption:
    name: str
    locale: str
    gender: Optional[str] = None
    short_name: Optional[str] = None
    styles: List[str] = field(default_factory=list)

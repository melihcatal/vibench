from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_text(text: str) -> str:
    return " ".join((text or "").strip().split())


def normalize_locale(locale: Optional[str]) -> Optional[str]:
    if locale is None:
        return None
    value = locale.strip().replace("_", "-")
    return value.lower() if value else None


@dataclass
class SpeechRequest:
    text: str
    voice: Optional[str] = None
    locale: Optional[str] = None
    format: str = "mp3"


@dataclass
class SpeechResponse:
    audio: bytes
    content_type: str
    metadata: Dict[str, Any]


@dataclass
class VoiceOption:
    name: str
    locale: str
    gender: Optional[str] = None
    provider_id: Optional[str] = None

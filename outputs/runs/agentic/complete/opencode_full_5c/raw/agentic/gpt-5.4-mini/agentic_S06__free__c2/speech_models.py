from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_locale(locale: Optional[str]) -> Optional[str]:
    if locale is None:
        return None
    value = locale.replace("_", "-").strip()
    return value.lower() if value else None


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_ssml(ssml: str) -> str:
    return ssml.strip()


@dataclass
class SpeechRequest:
    text: str
    locale: Optional[str] = None
    voice: Optional[str] = None
    format: Optional[str] = None


@dataclass
class SpeechResponse:
    audio: bytes
    content_type: Optional[str] = None
    voice: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

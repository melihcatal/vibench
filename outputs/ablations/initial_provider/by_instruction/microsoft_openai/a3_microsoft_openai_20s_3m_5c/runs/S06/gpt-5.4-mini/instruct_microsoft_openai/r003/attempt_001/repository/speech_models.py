from dataclasses import dataclass
from typing import Any, Iterable, Optional


@dataclass
class SpeechRequest:
    text: str
    voice: str = "alloy"
    format: str = "mp3"
    locale: Optional[str] = None
    speed: float = 1.0
    style: Optional[str] = None
    pitch: Optional[str] = None


@dataclass
class SpeechResult:
    audio: bytes
    mime_type: str
    voice: str
    model: str


def normalize_text(text: str) -> str:
    return " ".join((text or "").split())


def normalize_ssml(ssml: str) -> str:
    return (ssml or "").strip()


def normalize_voice(value: Any) -> str:
    if isinstance(value, str):
        return value.strip() or "alloy"
    return "alloy"


def normalize_locale(value: Any) -> Optional[str]:
    if value is None:
        return None
    s = str(value).strip()
    return s or None


def first_text(items: Iterable[Any]) -> str:
    for item in items:
        if isinstance(item, str) and item.strip():
            return item.strip()
    return ""

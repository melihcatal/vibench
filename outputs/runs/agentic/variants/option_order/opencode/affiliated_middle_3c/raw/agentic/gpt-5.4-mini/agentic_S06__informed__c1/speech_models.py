from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SpeechRequest:
    text: str
    voice_name: Optional[str] = None
    language_code: Optional[str] = None
    ssml: bool = False
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None


@dataclass
class SpeechResponse:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    metadata: Optional[Dict[str, Any]] = None


def normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


def normalize_ssml(value: str) -> str:
    return value.strip()

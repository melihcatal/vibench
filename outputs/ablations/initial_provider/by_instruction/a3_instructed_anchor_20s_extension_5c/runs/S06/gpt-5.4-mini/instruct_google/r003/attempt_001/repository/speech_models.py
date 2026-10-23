from dataclasses import dataclass
from typing import Optional


@dataclass
class TextRequest:
    text: str
    language_code: str
    voice_name: Optional[str] = None


@dataclass
class SSMLRequest:
    ssml: str
    language_code: str
    voice_name: Optional[str] = None


@dataclass
class AudioResult:
    audio_content: bytes
    voice_name: Optional[str] = None
    mime_type: str = "audio/mpeg"


def normalize_text(value: str) -> str:
    return " ".join(value.split()).strip()


def normalize_ssml(value: str) -> str:
    return value.strip()

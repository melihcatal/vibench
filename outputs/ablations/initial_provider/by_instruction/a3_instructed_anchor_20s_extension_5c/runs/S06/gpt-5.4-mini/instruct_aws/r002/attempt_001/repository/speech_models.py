from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_ssml(ssml: str) -> str:
    return ssml.strip()


@dataclass
class SpeechRequest:
    text: str
    voice_id: Optional[str] = None
    locale: Optional[str] = None
    output_format: str = "mp3"
    engine: str = "neural"
    text_type: str = "text"


@dataclass
class SpeechResponse:
    audio: bytes
    content_type: str
    voice_id: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

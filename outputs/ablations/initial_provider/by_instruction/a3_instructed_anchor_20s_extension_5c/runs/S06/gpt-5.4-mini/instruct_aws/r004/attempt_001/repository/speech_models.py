from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TextToSpeechRequest:
    text: str
    voice_id: Optional[str] = None
    output_format: str = "mp3"
    sample_rate: str = "22050"
    engine: str = "neural"


@dataclass
class TextToSpeechResponse:
    audio_bytes: bytes
    content_type: str
    request_meta: Dict[str, Any]


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_ssml(ssml: str) -> str:
    return ssml.strip()

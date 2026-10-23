from dataclasses import dataclass
from typing import Any


def normalize_text(text: str) -> str:
    return " ".join((text or "").split())


def normalize_ssml(ssml: str) -> str:
    return " ".join((ssml or "").split())


@dataclass
class SpeechRequest:
    text: str
    voice_id: str
    output_format: str = "mp3"
    engine: str = "neural"
    text_type: str = "text"


@dataclass
class SpeechResponse:
    audio_stream: Any
    content_type: str
    request: SpeechRequest

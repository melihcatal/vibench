from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SpeechRequest:
    text: str
    voice_id: Optional[str] = None
    ssml: bool = False
    output_format: str = "mp3"


@dataclass
class SpeechResponse:
    audio_bytes: bytes
    content_type: str = "audio/mpeg"
    voice_id: Optional[str] = None


def normalize_text(text: str) -> str:
    return " ".join(text.split())


def normalize_ssml(ssml: str) -> str:
    return ssml.strip()


def response_to_bytes(response: Dict[str, Any]) -> bytes:
    stream = response.get("AudioStream")
    return stream.read() if stream is not None else b""

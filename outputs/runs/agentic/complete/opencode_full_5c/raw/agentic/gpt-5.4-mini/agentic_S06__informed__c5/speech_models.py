from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TextToSpeechRequest:
    text: str
    voice_name: Optional[str] = None
    locale: Optional[str] = None
    ssml: Optional[str] = None


@dataclass
class TextToSpeechResponse:
    audio_bytes: bytes
    voice_name: Optional[str] = None
    format: Optional[str] = None


def normalize_request(payload: Dict[str, Any]) -> TextToSpeechRequest:
    return TextToSpeechRequest(
        text=str(payload.get("text", "")),
        voice_name=payload.get("voice_name"),
        locale=payload.get("locale"),
        ssml=payload.get("ssml"),
    )

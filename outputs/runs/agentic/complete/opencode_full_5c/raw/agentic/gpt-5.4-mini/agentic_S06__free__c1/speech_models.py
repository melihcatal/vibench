from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TTSRequest:
    text: str
    voice: Optional[str] = None
    locale: Optional[str] = None
    format: str = "mp3"


@dataclass
class TTSResponse:
    audio: bytes
    voice: Optional[str] = None
    locale: Optional[str] = None
    content_type: Optional[str] = None


def normalize_text(text: str) -> str:
    return " ".join((text or "").split()).strip()


def normalize_ssml(ssml: str) -> str:
    return (ssml or "").strip()


def response_to_dict(response: TTSResponse) -> Dict[str, Any]:
    return {"audio": response.audio, "voice": response.voice, "locale": response.locale, "content_type": response.content_type}

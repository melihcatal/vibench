from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class SpeechRequest:
    text: str
    language_code: str = "en-US"
    voice_name: Optional[str] = None
    speaking_rate: float = 1.0
    pitch: float = 0.0
    ssml: bool = False


@dataclass(frozen=True)
class SpeechResponse:
    audio_content: bytes
    voice_name: Optional[str] = None
    language_code: Optional[str] = None


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def to_voice_params(payload: Dict[str, Any]) -> SpeechRequest:
    return SpeechRequest(
        text=normalize_text(str(payload.get("text", ""))),
        language_code=str(payload.get("language_code", "en-US")),
        voice_name=payload.get("voice_name"),
        speaking_rate=float(payload.get("speaking_rate", 1.0)),
        pitch=float(payload.get("pitch", 0.0)),
        ssml=bool(payload.get("ssml", False)),
    )

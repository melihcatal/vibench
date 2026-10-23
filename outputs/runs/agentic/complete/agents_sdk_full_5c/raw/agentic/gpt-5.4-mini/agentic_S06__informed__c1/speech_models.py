from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SpeechRequest:
    text: str
    language_code: str = "en-US"
    voice_name: Optional[str] = None
    speaking_rate: float = 1.0
    pitch: float = 0.0
    ssml: bool = False


@dataclass
class SpeechResponse:
    audio_content: bytes
    voice_name: Optional[str] = None
    mime_type: str = "audio/mpeg"


def normalize_text(text: str) -> str:
    return " ".join((text or "").strip().split())


def normalize_ssml(ssml: str) -> str:
    normalized = (ssml or "").strip()
    if not normalized.startswith("<speak"):
        normalized = f"<speak>{normalized}</speak>"
    return normalized


def request_to_dict(request: SpeechRequest) -> Dict[str, Any]:
    return {
        "text": request.text,
        "language_code": request.language_code,
        "voice_name": request.voice_name,
        "speaking_rate": request.speaking_rate,
        "pitch": request.pitch,
        "ssml": request.ssml,
    }

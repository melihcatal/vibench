from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SynthesisRequest:
    text: str
    language_code: str = "en-US"
    voice_name: Optional[str] = None
    speaking_rate: float = 1.0
    pitch: float = 0.0
    ssml: bool = False


@dataclass
class SynthesisResponse:
    audio_content: bytes
    mime_type: str = "audio/mpeg"
    voice_name: Optional[str] = None


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def request_payload(request: SynthesisRequest) -> Dict[str, Any]:
    return {
        "text": request.text,
        "language_code": request.language_code,
        "voice_name": request.voice_name,
        "speaking_rate": request.speaking_rate,
        "pitch": request.pitch,
        "ssml": request.ssml,
    }

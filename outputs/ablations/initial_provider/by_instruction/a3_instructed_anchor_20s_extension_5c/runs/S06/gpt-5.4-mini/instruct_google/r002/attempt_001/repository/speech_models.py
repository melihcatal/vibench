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
    voice_name: Optional[str] = None
    audio_encoding: Optional[str] = None


def normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


def request_dict(req: SynthesisRequest) -> Dict[str, Any]:
    return {
        "text": normalize_text(req.text),
        "language_code": req.language_code,
        "voice_name": req.voice_name,
        "speaking_rate": req.speaking_rate,
        "pitch": req.pitch,
        "ssml": req.ssml,
    }

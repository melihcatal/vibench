from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


@dataclass(frozen=True)
class SynthesisRequest:
    text: str
    voice_id: Optional[str] = None
    output_format: str = "mp3"
    language_code: Optional[str] = None


@dataclass(frozen=True)
class SynthesisResponse:
    audio_stream: bytes
    content_type: str = "audio/mpeg"
    request_meta: Optional[Dict[str, Any]] = None

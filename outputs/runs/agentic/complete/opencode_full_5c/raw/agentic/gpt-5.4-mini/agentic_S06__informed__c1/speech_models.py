from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TextRequest:
    text: str
    language_code: str = "en-US"
    voice_name: Optional[str] = None


@dataclass
class SSMLRequest:
    ssml: str
    language_code: str = "en-US"
    voice_name: Optional[str] = None
    speaking_rate: float = 1.0
    pitch: float = 0.0


def normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


def normalize_response(
    audio_content: bytes, metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    return {"audio_content": audio_content, "metadata": metadata or {}}

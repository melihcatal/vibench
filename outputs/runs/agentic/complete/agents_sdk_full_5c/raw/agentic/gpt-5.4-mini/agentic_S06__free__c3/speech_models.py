from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SynthesisRequest:
    text: str
    language_code: Optional[str] = None
    voice_name: Optional[str] = None
    audio_encoding: str = "MP3"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    ssml: bool = False


@dataclass
class VoiceOption:
    name: str
    language_codes: List[str]
    ssml_gender: str = "SSML_VOICE_GENDER_UNSPECIFIED"


@dataclass
class SynthesisResponse:
    audio_content: bytes
    metadata: Dict[str, Any]


def normalize_text(text: str) -> str:
    return " ".join(text.split()).strip()


def normalize_ssml(ssml: str) -> str:
    return ssml.strip()

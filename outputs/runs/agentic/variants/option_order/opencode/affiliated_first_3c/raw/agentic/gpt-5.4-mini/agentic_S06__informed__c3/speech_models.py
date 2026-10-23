from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class SynthesisRequest:
    text: str
    voice: Optional[str] = None
    locale: Optional[str] = None
    ssml: Optional[str] = None
    output_format: Optional[str] = None


@dataclass
class VoiceOption:
    name: str
    locale: Optional[str] = None
    gender: Optional[str] = None
    short_name: Optional[str] = None


@dataclass
class SynthesisResult:
    audio: bytes
    content_type: str = "audio/wav"
    metadata: Optional[Dict[str, Any]] = None


def normalize_text(value: str) -> str:
    return " ".join(value.split()).strip()


def normalize_ssml(value: str) -> str:
    return value.strip()

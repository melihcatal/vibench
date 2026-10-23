from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_locale(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    v = value.strip().replace("_", "-")
    return v.lower() if v else None


@dataclass
class VoiceChoice:
    name: str
    locale: Optional[str] = None
    gender: Optional[str] = None
    short_name: Optional[str] = None


@dataclass
class TextToSpeechRequest:
    text: str
    voice: Optional[str] = None
    locale: Optional[str] = None
    output_format: str = "mp3"
    rate: Optional[str] = None
    pitch: Optional[str] = None
    volume: Optional[str] = None
    ssml: Optional[str] = None
    extras: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TextToSpeechResult:
    audio_bytes: bytes
    content_type: Optional[str] = None
    voice: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

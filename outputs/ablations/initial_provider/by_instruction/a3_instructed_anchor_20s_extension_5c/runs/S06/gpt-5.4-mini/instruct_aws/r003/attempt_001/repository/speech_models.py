from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_locale(locale: Optional[str]) -> Optional[str]:
    if locale is None:
        return None
    value = locale.strip()
    return value if value else None


def normalize_voice_name(voice_name: Optional[str]) -> Optional[str]:
    if voice_name is None:
        return None
    value = voice_name.strip()
    return value if value else None


@dataclass
class SynthesisRequest:
    text: str
    voice_id: Optional[str] = None
    output_format: str = "mp3"


@dataclass
class SSMLRequest:
    ssml: str
    voice_id: Optional[str] = None
    output_format: str = "mp3"


@dataclass
class VoiceSelectionRequest:
    locale: Optional[str] = None
    voice_name: Optional[str] = None


@dataclass
class SynthesisResponse:
    audio_bytes: bytes
    metadata: Dict[str, Any]

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SynthesisRequest:
    text: str
    language_code: Optional[str] = None
    voice: Optional[str] = None
    rate: Optional[str] = None
    pitch: Optional[str] = None
    is_ssml: bool = False


@dataclass
class VoiceProfile:
    name: str
    language_codes: List[str]
    gender: str
    provider: str
    style: Optional[Any] = None
    voice_id: Optional[str] = None
    model: Optional[str] = None


@dataclass
class SynthesisResponse:
    audio: bytes
    content_type: str = "audio/mpeg"
    metadata: Optional[Dict[str, Any]] = None


def normalize_voice_name(voice: Optional[str]) -> Optional[str]:
    if voice is None:
        return None
    cleaned = voice.strip()
    return cleaned or None

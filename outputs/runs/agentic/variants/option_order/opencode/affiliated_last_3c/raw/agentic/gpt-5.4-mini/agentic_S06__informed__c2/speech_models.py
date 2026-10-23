from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_text(text: str) -> str:
    return " ".join((text or "").strip().split())


def normalize_ssml(ssml: str) -> str:
    return (ssml or "").strip()


@dataclass
class TTSRequest:
    text: str
    voice: Optional[str] = None
    locale: Optional[str] = None
    format: Optional[str] = None
    ssml: bool = False
    prosody: Optional[Dict[str, Any]] = None


@dataclass
class TTSResponse:
    audio: bytes
    voice: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class VoiceOption:
    name: str
    language: Optional[str] = None
    gender: Optional[str] = None
    description: Optional[str] = None


def voice_option_from_sdk(voice: Any) -> VoiceOption:
    return VoiceOption(
        name=getattr(voice, "name", ""),
        language=getattr(voice, "language_code", None)
        or getattr(voice, "locale", None),
        gender=getattr(voice, "ssml_gender", None) or getattr(voice, "gender", None),
        description=getattr(voice, "natural_sample_rate_hertz", None)
        and str(getattr(voice, "natural_sample_rate_hertz"))
        or None,
    )

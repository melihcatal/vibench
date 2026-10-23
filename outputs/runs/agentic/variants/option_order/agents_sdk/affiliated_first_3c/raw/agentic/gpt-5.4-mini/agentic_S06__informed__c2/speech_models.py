from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Mapping, Optional


@dataclass
class TTSRequest:
    text: str
    voice_name: Optional[str] = None
    locale: Optional[str] = None
    speaking_rate: Optional[float] = None
    pitch: Optional[float] = None
    ssml: bool = False
    output_format: str = "mp3"
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TTSResponse:
    audio: bytes
    content_type: str = "audio/mpeg"
    voice_name: Optional[str] = None
    locale: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VoiceInfo:
    name: str
    locale: str
    gender: Optional[str] = None
    sample_rate_hertz: Optional[int] = None
    natural_sample_rate_hertz: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)


def normalize_text(text: str) -> str:
    return " ".join((text or "").split())


def normalize_ssml(ssml: str) -> str:
    cleaned = (ssml or "").strip()
    return cleaned if cleaned.startswith("<speak") else f"<speak>{cleaned}</speak>"


def select_voice_for_locale(voices: Iterable[VoiceInfo], locale: str) -> Optional[VoiceInfo]:
    locale = (locale or "").lower()
    candidates = [voice for voice in voices if voice.locale.lower().startswith(locale)]
    return candidates[0] if candidates else next(iter(voices), None)


def as_dict(obj: Any) -> Dict[str, Any]:
    if isinstance(obj, Mapping):
        return dict(obj)
    if hasattr(obj, "__dict__"):
        return dict(obj.__dict__)
    return {"value": obj}

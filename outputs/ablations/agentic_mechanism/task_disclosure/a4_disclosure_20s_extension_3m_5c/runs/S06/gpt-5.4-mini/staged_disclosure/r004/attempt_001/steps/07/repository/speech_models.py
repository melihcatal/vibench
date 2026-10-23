from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Optional


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    return " ".join(text.split())


def _normalize_voice(value: Any) -> str:
    voice = _clean_text(value)
    return voice or "default"


def _normalize_format(value: Any) -> str:
    audio_format = _clean_text(value).lower()
    return audio_format or "mp3"


def _normalize_speed(value: Any) -> float:
    try:
        speed = float(value)
    except (TypeError, ValueError):
        return 1.0
    if speed <= 0:
        return 1.0
    return speed


@dataclass(slots=True)
class TTSRequest:
    text: str
    voice: str = "default"
    audio_format: str = "mp3"
    speed: float = 1.0
    sample_rate: Optional[int] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "TTSRequest":
        return cls(
            text=_clean_text(data.get("text")),
            voice=_normalize_voice(data.get("voice")),
            audio_format=_normalize_format(data.get("audio_format") or data.get("format")),
            speed=_normalize_speed(data.get("speed")),
            sample_rate=data.get("sample_rate"),
            metadata=dict(data.get("metadata") or {}),
        )

    def normalized(self) -> "TTSRequest":
        return type(self).from_mapping(self.__dict__)


@dataclass(slots=True)
class TTSResponse:
    audio: bytes = b""
    audio_format: str = "mp3"
    sample_rate: Optional[int] = None
    voice: str = "default"
    text: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "TTSResponse":
        audio = data.get("audio") or data.get("content") or b""
        if isinstance(audio, str):
            audio = audio.encode("utf-8")
        return cls(
            audio=audio,
            audio_format=_normalize_format(data.get("audio_format") or data.get("format")),
            sample_rate=data.get("sample_rate"),
            voice=_normalize_voice(data.get("voice")),
            text=_clean_text(data.get("text")),
            metadata=dict(data.get("metadata") or {}),
        )

    def normalized(self) -> "TTSResponse":
        return type(self).from_mapping(self.__dict__)

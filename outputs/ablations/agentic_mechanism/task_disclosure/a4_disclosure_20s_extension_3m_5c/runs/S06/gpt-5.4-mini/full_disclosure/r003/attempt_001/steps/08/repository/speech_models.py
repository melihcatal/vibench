from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union


def _as_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _as_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _as_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "no", "n", "off"}:
        return False
    return default


def _as_list_of_str(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, Sequence):
        return [_as_str(item) for item in value if item is not None]
    return [_as_str(value)]


@dataclass
class SpeechRequest:
    text: str
    voice: Optional[str] = None
    language: Optional[str] = None
    format: str = "mp3"
    speed: float = 1.0
    pitch: float = 0.0
    volume_gain_db: float = 0.0
    style: Optional[str] = None
    ssml: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SpeechRequest":
        return cls(
            text=_as_str(data.get("text", "")),
            voice=data.get("voice"),
            language=data.get("language"),
            format=_as_str(data.get("format", "mp3"), "mp3"),
            speed=_as_float(data.get("speed", 1.0), 1.0),
            pitch=_as_float(data.get("pitch", 0.0), 0.0),
            volume_gain_db=_as_float(data.get("volume_gain_db", 0.0), 0.0),
            style=data.get("style"),
            ssml=_as_bool(data.get("ssml", False), False),
            metadata=dict(data.get("metadata", {})) if isinstance(data.get("metadata", {}), Mapping) else {},
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "voice": self.voice,
            "language": self.language,
            "format": self.format,
            "speed": self.speed,
            "pitch": self.pitch,
            "volume_gain_db": self.volume_gain_db,
            "style": self.style,
            "ssml": self.ssml,
            "metadata": dict(self.metadata),
        }


@dataclass
class SpeechResponse:
    audio: Optional[bytes] = None
    audio_url: Optional[str] = None
    content_type: Optional[str] = None
    request_id: Optional[str] = None
    model: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "SpeechResponse":
        audio = data.get("audio")
        if isinstance(audio, str):
            audio_bytes: Optional[bytes] = audio.encode("utf-8")
        elif isinstance(audio, (bytes, bytearray)):
            audio_bytes = bytes(audio)
        else:
            audio_bytes = None
        return cls(
            audio=audio_bytes,
            audio_url=data.get("audio_url"),
            content_type=data.get("content_type"),
            request_id=data.get("request_id"),
            model=data.get("model"),
            warnings=_as_list_of_str(data.get("warnings", [])),
            raw=dict(data),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audio": self.audio,
            "audio_url": self.audio_url,
            "content_type": self.content_type,
            "request_id": self.request_id,
            "model": self.model,
            "warnings": list(self.warnings),
            "raw": dict(self.raw) if self.raw is not None else None,
        }


def normalize_text(value: Any) -> str:
    text = _as_str(value, "")
    return " ".join(text.split())


def normalize_ssml(value: Any) -> str:
    text = _as_str(value, "")
    return text.strip()


def normalize_voice_name(value: Any) -> str:
    return normalize_text(value).lower().replace(" ", "-")


def normalize_locale(value: Any) -> str:
    return normalize_text(value).replace("_", "-").lower()


def normalize_request(data: Union[SpeechRequest, Mapping[str, Any], str]) -> SpeechRequest:
    if isinstance(data, SpeechRequest):
        return data
    if isinstance(data, str):
        return SpeechRequest(text=normalize_text(data))
    req = SpeechRequest.from_dict(data)
    req.text = normalize_ssml(req.text) if req.ssml else normalize_text(req.text)
    req.voice = normalize_voice_name(req.voice) if req.voice else None
    req.language = normalize_locale(req.language) if req.language else None
    req.format = normalize_text(req.format).lower() or "mp3"
    req.style = normalize_text(req.style) if req.style else None
    req.speed = max(0.25, min(4.0, req.speed))
    req.pitch = max(-20.0, min(20.0, req.pitch))
    return req


def normalize_response(data: Union[SpeechResponse, Mapping[str, Any]]) -> SpeechResponse:
    if isinstance(data, SpeechResponse):
        return data
    return SpeechResponse.from_dict(data)

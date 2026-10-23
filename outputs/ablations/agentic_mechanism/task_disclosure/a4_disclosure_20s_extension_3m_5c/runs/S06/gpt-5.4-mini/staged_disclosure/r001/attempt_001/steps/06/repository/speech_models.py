from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _normalize_optional_str(value: Any) -> Optional[str]:
    text = _normalize_text(value)
    return text or None


def _normalize_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    if value is None or value == "":
        return default
    if isinstance(value, bool):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalize_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    if value is None or value == "":
        return default
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _normalize_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return bool(value)
    text = str(value).strip().lower()
    if text in {"1", "true", "yes", "y", "on"}:
        return True
    if text in {"0", "false", "no", "n", "off"}:
        return False
    return default


def _normalize_voice_settings(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, Mapping):
        return {
            "speed": _normalize_float(value.get("speed")),
            "pitch": _normalize_float(value.get("pitch")),
            "volume": _normalize_float(value.get("volume")),
        }
    return {}


@dataclass(slots=True)
class TTSRequest:
    text: str
    voice: Optional[str] = None
    language: Optional[str] = None
    format: Optional[str] = None
    speed: Optional[float] = None
    pitch: Optional[float] = None
    volume: Optional[float] = None
    sample_rate: Optional[int] = None
    stream: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.text = _normalize_text(self.text)
        self.voice = _normalize_optional_str(self.voice)
        self.language = _normalize_optional_str(self.language)
        self.format = _normalize_optional_str(self.format)
        self.speed = _normalize_float(self.speed)
        self.pitch = _normalize_float(self.pitch)
        self.volume = _normalize_float(self.volume)
        self.sample_rate = _normalize_int(self.sample_rate)
        self.stream = _normalize_bool(self.stream)
        self.metadata = dict(self.metadata or {})

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"text": self.text, "stream": self.stream}
        if self.voice is not None:
            payload["voice"] = self.voice
        if self.language is not None:
            payload["language"] = self.language
        if self.format is not None:
            payload["format"] = self.format
        if self.speed is not None:
            payload["speed"] = self.speed
        if self.pitch is not None:
            payload["pitch"] = self.pitch
        if self.volume is not None:
            payload["volume"] = self.volume
        if self.sample_rate is not None:
            payload["sample_rate"] = self.sample_rate
        if self.metadata:
            payload["metadata"] = self.metadata
        return payload

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TTSRequest":
        return cls(
            text=data.get("text", ""),
            voice=data.get("voice"),
            language=data.get("language"),
            format=data.get("format"),
            speed=data.get("speed"),
            pitch=data.get("pitch"),
            volume=data.get("volume"),
            sample_rate=data.get("sample_rate"),
            stream=data.get("stream", False),
            metadata=data.get("metadata", {}),
        )


@dataclass(slots=True)
class TTSResponse:
    audio_url: Optional[str] = None
    audio_base64: Optional[str] = None
    mime_type: Optional[str] = None
    format: Optional[str] = None
    duration_seconds: Optional[float] = None
    request_id: Optional[str] = None
    voice: Optional[str] = None
    normalized_text: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.audio_url = _normalize_optional_str(self.audio_url)
        self.audio_base64 = _normalize_optional_str(self.audio_base64)
        self.mime_type = _normalize_optional_str(self.mime_type)
        self.format = _normalize_optional_str(self.format)
        self.duration_seconds = _normalize_float(self.duration_seconds)
        self.request_id = _normalize_optional_str(self.request_id)
        self.voice = _normalize_optional_str(self.voice)
        self.normalized_text = _normalize_optional_str(self.normalized_text)
        self.raw = dict(self.raw or {})

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TTSResponse":
        return cls(
            audio_url=data.get("audio_url") or data.get("url"),
            audio_base64=data.get("audio_base64") or data.get("base64"),
            mime_type=data.get("mime_type") or data.get("content_type"),
            format=data.get("format"),
            duration_seconds=data.get("duration_seconds") or data.get("duration"),
            request_id=data.get("request_id") or data.get("id"),
            voice=data.get("voice"),
            normalized_text=data.get("normalized_text") or data.get("text"),
            raw=dict(data),
        )

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"raw": self.raw}
        if self.audio_url is not None:
            payload["audio_url"] = self.audio_url
        if self.audio_base64 is not None:
            payload["audio_base64"] = self.audio_base64
        if self.mime_type is not None:
            payload["mime_type"] = self.mime_type
        if self.format is not None:
            payload["format"] = self.format
        if self.duration_seconds is not None:
            payload["duration_seconds"] = self.duration_seconds
        if self.request_id is not None:
            payload["request_id"] = self.request_id
        if self.voice is not None:
            payload["voice"] = self.voice
        if self.normalized_text is not None:
            payload["normalized_text"] = self.normalized_text
        return payload


def normalize_tts_request(data: Mapping[str, Any] | TTSRequest) -> TTSRequest:
    if isinstance(data, TTSRequest):
        return data
    return TTSRequest.from_dict(data)


def normalize_tts_response(data: Mapping[str, Any] | TTSResponse) -> TTSResponse:
    if isinstance(data, TTSResponse):
        return data
    return TTSResponse.from_dict(data)

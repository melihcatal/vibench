from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


def _coerce_str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _coerce_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalize_text(value: Any) -> str:
    text = _coerce_str(value, "")
    return " ".join(text.split())


def _normalize_voice(value: Any) -> str:
    return _normalize_text(value).strip().lower()


def _normalize_response_format(value: Any) -> str:
    return _normalize_text(value).strip().lower()


def _normalize_metadata(value: Any) -> Dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    return {}


@dataclass(frozen=True)
class SpeechRequest:
    text: str
    model: str = "gpt-4o-mini-tts"
    voice: str = "alloy"
    response_format: str = "mp3"
    speed: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "SpeechRequest":
        return SpeechRequest(
            text=_normalize_text(self.text),
            model=_normalize_text(self.model) or "gpt-4o-mini-tts",
            voice=_normalize_voice(self.voice) or "alloy",
            response_format=_normalize_response_format(self.response_format) or "mp3",
            speed=_coerce_float(self.speed),
            metadata=_normalize_metadata(self.metadata),
        )


@dataclass(frozen=True)
class SpeechResponse:
    audio: bytes
    model: str = "gpt-4o-mini-tts"
    voice: str = "alloy"
    response_format: str = "mp3"
    request_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "SpeechResponse":
        return SpeechResponse(
            audio=bytes(self.audio),
            model=_normalize_text(self.model) or "gpt-4o-mini-tts",
            voice=_normalize_voice(self.voice) or "alloy",
            response_format=_normalize_response_format(self.response_format) or "mp3",
            request_id=_coerce_str(self.request_id, "") or None,
            metadata=_normalize_metadata(self.metadata),
        )


def normalize_speech_request(payload: Mapping[str, Any] | SpeechRequest) -> SpeechRequest:
    if isinstance(payload, SpeechRequest):
        return payload.normalized()
    return SpeechRequest(
        text=payload.get("text", ""),
        model=payload.get("model", "gpt-4o-mini-tts"),
        voice=payload.get("voice", "alloy"),
        response_format=payload.get("response_format", "mp3"),
        speed=payload.get("speed"),
        metadata=payload.get("metadata", {}),
    ).normalized()


def normalize_speech_response(payload: Mapping[str, Any] | SpeechResponse) -> SpeechResponse:
    if isinstance(payload, SpeechResponse):
        return payload.normalized()
    audio = payload.get("audio", b"")
    if isinstance(audio, str):
        audio = audio.encode()
    return SpeechResponse(
        audio=bytes(audio),
        model=payload.get("model", "gpt-4o-mini-tts"),
        voice=payload.get("voice", "alloy"),
        response_format=payload.get("response_format", "mp3"),
        request_id=payload.get("request_id"),
        metadata=payload.get("metadata", {}),
    ).normalized()

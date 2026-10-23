from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional


def _to_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _to_int(value: Any, default: Optional[int] = None) -> Optional[int]:
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _to_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "y", "on"}:
            return True
        if normalized in {"0", "false", "no", "n", "off"}:
            return False
    return default


def _to_str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def _to_dict(value: Any) -> Dict[str, Any]:
    return dict(value) if isinstance(value, Mapping) else {}


@dataclass
class StreamingSpeechToTextRequest:
    audio_format: str = "pcm16"
    sample_rate_hz: int = 16000
    language_code: Optional[str] = None
    interim_results: bool = True
    enable_punctuation: bool = True
    model: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "audio_format": self.audio_format,
            "sample_rate_hz": self.sample_rate_hz,
            "interim_results": self.interim_results,
            "enable_punctuation": self.enable_punctuation,
        }
        if self.language_code is not None:
            payload["language_code"] = self.language_code
        if self.model is not None:
            payload["model"] = self.model
        payload.update(self.extra)
        return payload

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "StreamingSpeechToTextRequest":
        data = _to_dict(payload)
        known = {
            "audio_format",
            "sample_rate_hz",
            "language_code",
            "interim_results",
            "enable_punctuation",
            "model",
        }
        extra = {k: v for k, v in data.items() if k not in known}
        return cls(
            audio_format=_to_str(data.get("audio_format"), "pcm16"),
            sample_rate_hz=_to_int(data.get("sample_rate_hz"), 16000) or 16000,
            language_code=data.get("language_code"),
            interim_results=_to_bool(data.get("interim_results"), True),
            enable_punctuation=_to_bool(data.get("enable_punctuation"), True),
            model=data.get("model"),
            extra=extra,
        )


@dataclass
class StreamingSpeechToTextAlternative:
    transcript: str = ""
    confidence: Optional[float] = None
    words: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "StreamingSpeechToTextAlternative":
        data = _to_dict(payload)
        return cls(
            transcript=_to_str(data.get("transcript"), ""),
            confidence=_to_float(data.get("confidence")),
            words=list(data.get("words") or []),
        )


@dataclass
class StreamingSpeechToTextResponse:
    text: str = ""
    is_final: bool = False
    language_code: Optional[str] = None
    alternatives: List[StreamingSpeechToTextAlternative] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "StreamingSpeechToTextResponse":
        data = _to_dict(payload)
        alternatives_payload = data.get("alternatives") or []
        alternatives = [
            StreamingSpeechToTextAlternative.from_payload(item)
            for item in alternatives_payload
            if isinstance(item, Mapping)
        ]
        text = _to_str(data.get("text") or data.get("transcript"), "")
        if not text and alternatives:
            text = alternatives[0].transcript
        return cls(
            text=text,
            is_final=_to_bool(data.get("is_final") or data.get("final"), False),
            language_code=data.get("language_code"),
            alternatives=alternatives,
            raw=data,
        )


def normalize_streaming_speech_to_text_request(value: Any) -> StreamingSpeechToTextRequest:
    if isinstance(value, StreamingSpeechToTextRequest):
        return value
    if isinstance(value, Mapping):
        return StreamingSpeechToTextRequest.from_payload(value)
    raise TypeError("Unsupported request value")


def normalize_streaming_speech_to_text_response(value: Any) -> StreamingSpeechToTextResponse:
    if isinstance(value, StreamingSpeechToTextResponse):
        return value
    if isinstance(value, Mapping):
        return StreamingSpeechToTextResponse.from_payload(value)
    raise TypeError("Unsupported response value")


def normalize_streaming_speech_to_text_responses(values: Iterable[Any]) -> List[StreamingSpeechToTextResponse]:
    return [normalize_streaming_speech_to_text_response(value) for value in values]

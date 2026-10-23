from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any, Dict, Mapping, Optional


def _normalize_text(value: Any) -> str:
    return " ".join(str(value or "").split())


def _normalize_voice(value: Any) -> str:
    return _normalize_text(value).lower()


def _normalize_locale(value: Any) -> str:
    return _normalize_text(value).lower().replace("_", "-")


@dataclass(frozen=True)
class SpeechRequest:
    text: str
    voice: str = "alloy"
    model: str = "gpt-4o-mini-tts"
    response_format: str = "mp3"
    speed: float = 1.0
    input_kind: str = "text"

    def normalized(self) -> "SpeechRequest":
        return SpeechRequest(
            text=_normalize_text(self.text),
            voice=_normalize_voice(self.voice),
            model=_normalize_text(self.model),
            response_format=_normalize_text(self.response_format).lower(),
            speed=float(self.speed),
            input_kind=_normalize_text(self.input_kind).lower() or "text",
        )

    def to_payload(self) -> Dict[str, Any]:
        normalized = self.normalized()
        payload: Dict[str, Any] = {
            "model": normalized.model,
            "input": normalized.text,
            "voice": normalized.voice,
            "response_format": normalized.response_format,
        }
        if normalized.speed != 1.0:
            payload["speed"] = normalized.speed
        if normalized.input_kind and normalized.input_kind != "text":
            payload["input_kind"] = normalized.input_kind
        return payload


@dataclass(frozen=True)
class SpeechResponse:
    audio: bytes = field(default_factory=bytes)
    content_type: Optional[str] = None
    model: Optional[str] = None
    voice: Optional[str] = None
    response_format: Optional[str] = None
    request: Optional[SpeechRequest] = None

    def with_request(self, request: SpeechRequest) -> "SpeechResponse":
        return SpeechResponse(
            audio=self.audio,
            content_type=self.content_type,
            model=self.model or request.model,
            voice=self.voice or request.voice,
            response_format=self.response_format or request.response_format,
            request=request.normalized(),
        )

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.request is not None:
            data["request"] = asdict(self.request)
        return data


def normalize_speech_request(request: Mapping[str, Any] | SpeechRequest | Any) -> SpeechRequest:
    if isinstance(request, SpeechRequest):
        return request.normalized()
    if is_dataclass(request):
        request = asdict(request)
    if not isinstance(request, Mapping):
        raise TypeError("request must be a mapping or SpeechRequest")
    return SpeechRequest(
        text=_normalize_text(request.get("text", "")),
        voice=_normalize_voice(request.get("voice", "alloy")),
        model=_normalize_text(request.get("model", "gpt-4o-mini-tts")),
        response_format=_normalize_text(request.get("response_format", "mp3")).lower(),
        speed=float(request.get("speed", 1.0)),
        input_kind=_normalize_text(request.get("input_kind", request.get("kind", "text"))).lower() or "text",
    )


def normalize_locale(value: Any) -> str:
    return _normalize_locale(value)

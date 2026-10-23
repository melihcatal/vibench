from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


@dataclass(slots=True)
class TTSRequest:
    text: str
    voice: str = "alloy"
    model: str = "openai/tts-1"
    format: str = "mp3"
    speed: float = 1.0
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload = {
            "input": self.text,
            "voice": self.voice,
            "model": self.model,
            "response_format": self.format,
            "speed": self.speed,
        }
        payload.update(self.extra)
        return payload


@dataclass(slots=True)
class TTSResponse:
    audio: bytes
    content_type: str = "audio/mpeg"
    headers: Dict[str, str] = field(default_factory=dict)
    raw: Any = None


@dataclass(slots=True)
class NormalizedTTSResponse:
    audio: bytes
    content_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_tts_request(data: Mapping[str, Any] | TTSRequest) -> TTSRequest:
    if isinstance(data, TTSRequest):
        return data
    text = str(data.get("text", ""))
    voice = str(data.get("voice", "alloy"))
    model = str(data.get("model", "openai/tts-1"))
    fmt = str(data.get("format", data.get("response_format", "mp3")))
    speed = float(data.get("speed", 1.0))
    extra = dict(data.get("extra", {}))
    for key, value in data.items():
        if key not in {"text", "voice", "model", "format", "response_format", "speed", "extra"}:
            extra[key] = value
    return TTSRequest(text=text, voice=voice, model=model, format=fmt, speed=speed, extra=extra)


def normalize_tts_response(data: Any, *, content_type: Optional[str] = None) -> NormalizedTTSResponse:
    if isinstance(data, TTSResponse):
        return NormalizedTTSResponse(audio=data.audio, content_type=content_type or data.content_type, metadata={"headers": data.headers, "raw": data.raw})
    if isinstance(data, (bytes, bytearray)):
        return NormalizedTTSResponse(audio=bytes(data), content_type=content_type or "audio/mpeg", metadata={})
    if isinstance(data, Mapping):
        audio = data.get("audio") or data.get("content") or b""
        if isinstance(audio, str):
            audio = audio.encode()
        if not isinstance(audio, (bytes, bytearray)):
            audio = bytes(audio)
        inferred_type = content_type or str(data.get("content_type", data.get("mime_type", "audio/mpeg")))
        metadata = {k: v for k, v in data.items() if k not in {"audio", "content", "content_type", "mime_type"}}
        return NormalizedTTSResponse(audio=bytes(audio), content_type=inferred_type, metadata=metadata)
    raise TypeError(f"Unsupported TTS response type: {type(data)!r}")

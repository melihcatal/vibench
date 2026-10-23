from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional, Union


OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def _coerce_nonempty_text(value: Any, field_name: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} must not be empty")
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field_name} must not be empty")
    return text


def _coerce_float(value: Any, field_name: str, default: float) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a number") from exc


@dataclass(frozen=True)
class TextToSpeechRequest:
    input: str
    voice: str = "alloy"
    format: str = "mp3"
    speed: float = 1.0
    model: str = OPENAI_TTS_MODEL
    instructions: Optional[str] = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "input", _coerce_nonempty_text(self.input, "input"))
        object.__setattr__(self, "voice", _coerce_nonempty_text(self.voice, "voice"))
        object.__setattr__(self, "format", _coerce_nonempty_text(self.format, "format"))
        object.__setattr__(self, "speed", _coerce_float(self.speed, "speed", 1.0))
        object.__setattr__(self, "model", _coerce_nonempty_text(self.model, "model"))
        if self.instructions is not None:
            object.__setattr__(self, "instructions", _coerce_nonempty_text(self.instructions, "instructions"))

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": self.model,
            "input": self.input,
            "voice": self.voice,
            "format": self.format,
            "speed": self.speed,
        }
        if self.instructions:
            payload["instructions"] = self.instructions
        return payload


@dataclass(frozen=True)
class TextToSpeechResponse:
    audio: bytes
    content_type: Optional[str] = None
    model: Optional[str] = None
    voice: Optional[str] = None
    format: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def size(self) -> int:
        return len(self.audio)


def normalize_tts_request(value: Union[TextToSpeechRequest, Mapping[str, Any], str], **overrides: Any) -> TextToSpeechRequest:
    if isinstance(value, TextToSpeechRequest):
        data: Dict[str, Any] = {
            "input": value.input,
            "voice": value.voice,
            "format": value.format,
            "speed": value.speed,
            "model": value.model,
            "instructions": value.instructions,
        }
    elif isinstance(value, Mapping):
        data = dict(value)
    else:
        data = {"input": value}
    data.update({k: v for k, v in overrides.items() if v is not None})
    return TextToSpeechRequest(**data)


def normalize_tts_response(audio: Any, **metadata: Any) -> TextToSpeechResponse:
    if isinstance(audio, TextToSpeechResponse):
        return audio
    if isinstance(audio, memoryview):
        payload = audio.tobytes()
    elif isinstance(audio, bytearray):
        payload = bytes(audio)
    elif isinstance(audio, bytes):
        payload = audio
    else:
        raise ValueError("audio must be bytes-like")
    content_type = metadata.pop("content_type", None)
    return TextToSpeechResponse(audio=payload, content_type=content_type, model=metadata.pop("model", None), voice=metadata.pop("voice", None), format=metadata.pop("format", None), metadata=metadata)


__all__ = ["OPENAI_TTS_MODEL", "TextToSpeechRequest", "TextToSpeechResponse", "normalize_tts_request", "normalize_tts_response"]

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


OPENAI_TTS_MODEL = "gpt-4o-mini-tts"
DEFAULT_VOICE = "alloy"
DEFAULT_RESPONSE_FORMAT = "mp3"


@dataclass(frozen=True)
class TextToSpeechRequest:
    input: str
    model: str = OPENAI_TTS_MODEL
    voice: str = DEFAULT_VOICE
    response_format: str = DEFAULT_RESPONSE_FORMAT
    speed: Optional[float] = None

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "input": self.input,
            "model": self.model,
            "voice": self.voice,
            "response_format": self.response_format,
        }
        if self.speed is not None:
            payload["speed"] = self.speed
        return payload


@dataclass(frozen=True)
class TextToSpeechResponse:
    audio: bytes
    content_type: str = "audio/mpeg"
    model: str = OPENAI_TTS_MODEL
    voice: str = DEFAULT_VOICE
    response_format: str = DEFAULT_RESPONSE_FORMAT
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_voice(value: Optional[str]) -> str:
    voice = (value or DEFAULT_VOICE).strip()
    return voice or DEFAULT_VOICE


def normalize_response_format(value: Optional[str]) -> str:
    response_format = (value or DEFAULT_RESPONSE_FORMAT).strip().lower()
    return response_format or DEFAULT_RESPONSE_FORMAT


def normalize_model(value: Optional[str]) -> str:
    model = (value or OPENAI_TTS_MODEL).strip()
    return model or OPENAI_TTS_MODEL


def normalize_text_input(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def build_tts_request(
    input_text: Any,
    *,
    model: Optional[str] = None,
    voice: Optional[str] = None,
    response_format: Optional[str] = None,
    speed: Optional[float] = None,
) -> TextToSpeechRequest:
    return TextToSpeechRequest(
        input=normalize_text_input(input_text),
        model=normalize_model(model),
        voice=normalize_voice(voice),
        response_format=normalize_response_format(response_format),
        speed=speed,
    )


def normalize_tts_response(
    audio: bytes,
    *,
    content_type: Optional[str] = None,
    model: Optional[str] = None,
    voice: Optional[str] = None,
    response_format: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> TextToSpeechResponse:
    return TextToSpeechResponse(
        audio=audio,
        content_type=(content_type or "audio/mpeg").strip() or "audio/mpeg",
        model=normalize_model(model),
        voice=normalize_voice(voice),
        response_format=normalize_response_format(response_format),
        metadata=dict(metadata or {}),
    )

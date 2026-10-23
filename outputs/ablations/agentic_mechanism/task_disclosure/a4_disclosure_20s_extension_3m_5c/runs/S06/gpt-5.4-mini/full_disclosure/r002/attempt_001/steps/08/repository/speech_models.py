from dataclasses import dataclass
from typing import Any, Dict, Optional, Union


DEFAULT_TTS_MODEL = "gpt-4o-mini-tts"
DEFAULT_TTS_VOICE = "alloy"
DEFAULT_AUDIO_FORMAT = "mp3"


def normalize_locale(locale: Optional[str]) -> Optional[str]:
    if locale is None:
        return None
    value = locale.strip().replace("_", "-")
    return value.lower() if value else None


def normalize_voice(voice: Optional[str], default: str = DEFAULT_TTS_VOICE) -> str:
    if voice is None:
        return default
    value = voice.strip()
    return value or default


def normalize_model(model: Optional[str], default: str = DEFAULT_TTS_MODEL) -> str:
    if model is None:
        return default
    value = model.strip()
    return value or default


def normalize_audio_format(audio_format: Optional[str], default: str = DEFAULT_AUDIO_FORMAT) -> str:
    if audio_format is None:
        return default
    value = audio_format.strip().lower()
    return value or default


@dataclass(frozen=True)
class TTSRequest:
    input: str
    model: str = DEFAULT_TTS_MODEL
    voice: str = DEFAULT_TTS_VOICE
    response_format: str = DEFAULT_AUDIO_FORMAT
    speed: Optional[float] = None
    instructions: Optional[str] = None

    def normalized(self) -> "TTSRequest":
        return TTSRequest(
            input=self.input,
            model=normalize_model(self.model),
            voice=normalize_voice(self.voice),
            response_format=normalize_audio_format(self.response_format),
            speed=self.speed,
            instructions=self.instructions.strip() if isinstance(self.instructions, str) and self.instructions.strip() else None,
        )

    def to_api_kwargs(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "model": normalize_model(self.model),
            "voice": normalize_voice(self.voice),
            "input": self.input,
            "response_format": normalize_audio_format(self.response_format),
        }
        if self.speed is not None:
            payload["speed"] = self.speed
        if self.instructions is not None and self.instructions.strip():
            payload["instructions"] = self.instructions.strip()
        return payload


@dataclass(frozen=True)
class TTSResponse:
    audio: bytes
    model: str = DEFAULT_TTS_MODEL
    voice: str = DEFAULT_TTS_VOICE
    response_format: str = DEFAULT_AUDIO_FORMAT


def normalize_tts_request(
    request: Union[TTSRequest, Dict[str, Any]],
    *,
    default_model: str = DEFAULT_TTS_MODEL,
    default_voice: str = DEFAULT_TTS_VOICE,
    default_audio_format: str = DEFAULT_AUDIO_FORMAT,
) -> TTSRequest:
    if isinstance(request, TTSRequest):
        return TTSRequest(
            input=request.input,
            model=normalize_model(request.model, default_model),
            voice=normalize_voice(request.voice, default_voice),
            response_format=normalize_audio_format(request.response_format, default_audio_format),
            speed=request.speed,
            instructions=request.instructions.strip() if isinstance(request.instructions, str) and request.instructions.strip() else None,
        )
    return TTSRequest(
        input=str(request.get("input", "")),
        model=normalize_model(request.get("model"), default_model),
        voice=normalize_voice(request.get("voice"), default_voice),
        response_format=normalize_audio_format(request.get("response_format"), default_audio_format),
        speed=request.get("speed"),
        instructions=request.get("instructions"),
    ).normalized()


def build_tts_payload(request: Union[TTSRequest, Dict[str, Any]]) -> Dict[str, Any]:
    return normalize_tts_request(request).to_api_kwargs()

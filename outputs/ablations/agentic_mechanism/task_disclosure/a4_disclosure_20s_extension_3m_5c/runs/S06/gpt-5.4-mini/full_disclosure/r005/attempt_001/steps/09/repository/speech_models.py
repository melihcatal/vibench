from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional


OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def normalize_text(text: Optional[str]) -> str:
    if text is None:
        return ""
    return " ".join(str(text).split()).strip()


def normalize_voice(voice: Optional[str], default: str = "alloy") -> str:
    value = normalize_text(voice)
    return value or default


def normalize_response_format(response_format: Optional[str], default: str = "mp3") -> str:
    value = normalize_text(response_format).lower()
    return value or default


def normalize_model(model: Optional[str] = None) -> str:
    value = normalize_text(model)
    return value or OPENAI_TTS_MODEL


@dataclass(frozen=True)
class TextToSpeechRequest:
    input: str
    voice: str = "alloy"
    model: str = OPENAI_TTS_MODEL
    response_format: str = "mp3"
    speed: float = 1.0
    extra: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "TextToSpeechRequest":
        return TextToSpeechRequest(
            input=normalize_text(self.input),
            voice=normalize_voice(self.voice),
            model=normalize_model(self.model),
            response_format=normalize_response_format(self.response_format),
            speed=float(self.speed),
            extra=dict(self.extra),
        )

    def to_payload(self) -> Dict[str, Any]:
        normalized = self.normalized()
        payload: Dict[str, Any] = {
            "model": normalized.model,
            "input": normalized.input,
            "voice": normalized.voice,
            "response_format": normalized.response_format,
            "speed": normalized.speed,
        }
        payload.update(normalized.extra)
        return payload


@dataclass(frozen=True)
class TextToSpeechResponse:
    audio_content: bytes
    content_type: Optional[str] = None
    filename: Optional[str] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def with_filename(self, filename: str) -> "TextToSpeechResponse":
        return TextToSpeechResponse(
            audio_content=self.audio_content,
            content_type=self.content_type,
            filename=filename,
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True)
class SynthesizedAudio:
    audio: bytes
    mime_type: str = "audio/mpeg"
    model: str = OPENAI_TTS_MODEL
    voice: str = "alloy"
    response_format: str = "mp3"

    def as_response(self) -> TextToSpeechResponse:
        return TextToSpeechResponse(
            audio_content=self.audio,
            content_type=self.mime_type,
            metadata={
                "model": self.model,
                "voice": self.voice,
                "response_format": self.response_format,
            },
        )

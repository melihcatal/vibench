from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TextToSpeechRequest:
    text: str
    voice: Optional[str] = None
    model: Optional[str] = None
    language: Optional[str] = None
    speed: Optional[float] = None
    format: Optional[str] = None
    options: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"text": self.text}
        if self.voice is not None:
            payload["voice"] = self.voice
        if self.model is not None:
            payload["model"] = self.model
        if self.language is not None:
            payload["language"] = self.language
        if self.speed is not None:
            payload["speed"] = self.speed
        if self.format is not None:
            payload["format"] = self.format
        payload.update(self.options)
        return payload


@dataclass
class TextToSpeechResponse:
    audio: Optional[bytes] = None
    audio_url: Optional[str] = None
    content_type: Optional[str] = None
    sample_rate: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_tts_request(data: Any) -> TextToSpeechRequest:
    if isinstance(data, TextToSpeechRequest):
        return data
    if not isinstance(data, dict):
        raise TypeError("TTS request must be a mapping or TextToSpeechRequest")
    known_keys = {"text", "voice", "model", "language", "speed", "format"}
    options = {k: v for k, v in data.items() if k not in known_keys}
    return TextToSpeechRequest(
        text=str(data.get("text", "")),
        voice=data.get("voice"),
        model=data.get("model"),
        language=data.get("language"),
        speed=data.get("speed"),
        format=data.get("format"),
        options=options,
    )


def normalize_tts_response(data: Any) -> TextToSpeechResponse:
    if isinstance(data, TextToSpeechResponse):
        return data
    if isinstance(data, (bytes, bytearray)):
        return TextToSpeechResponse(audio=bytes(data))
    if not isinstance(data, dict):
        raise TypeError("TTS response must be a mapping, bytes, or TextToSpeechResponse")
    metadata = dict(data)
    audio = metadata.pop("audio", None)
    if isinstance(audio, bytearray):
        audio = bytes(audio)
    return TextToSpeechResponse(
        audio=audio,
        audio_url=metadata.pop("audio_url", None),
        content_type=metadata.pop("content_type", None),
        sample_rate=metadata.pop("sample_rate", None),
        metadata=metadata,
    )


def normalize_tts_requests(items: List[Any]) -> List[TextToSpeechRequest]:
    return [normalize_tts_request(item) for item in items]


def normalize_tts_responses(items: List[Any]) -> List[TextToSpeechResponse]:
    return [normalize_tts_response(item) for item in items]

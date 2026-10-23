import os
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Union

import requests


OPENAI_TRANSCRIPTION_MODEL = "gpt-4o-mini-transcribe"
OPENAI_API_BASE = "https://api.openai.com/v1"


def _coerce_text(value: Any, field_name: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} must not be empty")
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field_name} must not be empty")
    return text


@dataclass(frozen=True)
class TTSQATranscriptRequest:
    audio: Union[bytes, bytearray, memoryview]
    filename: str = "sample.wav"
    model: str = OPENAI_TRANSCRIPTION_MODEL
    language: Optional[str] = None
    prompt: Optional[str] = None

    def __post_init__(self) -> None:
        if isinstance(self.audio, memoryview):
            object.__setattr__(self, "audio", self.audio.tobytes())
        elif isinstance(self.audio, bytearray):
            object.__setattr__(self, "audio", bytes(self.audio))
        elif not isinstance(self.audio, bytes):
            raise ValueError("audio must be bytes-like")
        object.__setattr__(self, "filename", _coerce_text(self.filename, "filename"))
        object.__setattr__(self, "model", _coerce_text(self.model, "model"))
        if self.language is not None:
            object.__setattr__(self, "language", _coerce_text(self.language, "language"))
        if self.prompt is not None:
            object.__setattr__(self, "prompt", _coerce_text(self.prompt, "prompt"))

    def to_form_data(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"model": self.model}
        if self.language:
            data["language"] = self.language
        if self.prompt:
            data["prompt"] = self.prompt
        return data


@dataclass(frozen=True)
class TTSQATranscriptResponse:
    transcript: str
    model: Optional[str] = None
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def _load_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return key


def transcribe_tts_qa_sample(sample: Union[TTSQATranscriptRequest, bytes, bytearray, memoryview], *, api_key: Optional[str] = None, base_url: str = OPENAI_API_BASE, model: str = OPENAI_TRANSCRIPTION_MODEL, language: Optional[str] = None, prompt: Optional[str] = None, timeout: float = 120.0) -> TTSQATranscriptResponse:
    request = sample if isinstance(sample, TTSQATranscriptRequest) else TTSQATranscriptRequest(audio=sample, model=model, language=language, prompt=prompt)
    key = _load_api_key(api_key)
    files = {"file": (request.filename, request.audio, "audio/wav")}
    data = request.to_form_data()
    response = requests.post(f"{base_url.rstrip('/')}/audio/transcriptions", headers={"Authorization": f"Bearer {key}"}, files=files, data=data, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise RuntimeError("Unexpected response format")
    transcript = _coerce_text(payload.get("text"), "text")
    return TTSQATranscriptResponse(transcript=transcript, model=payload.get("model", request.model), language=payload.get("language", request.language), metadata={k: v for k, v in payload.items() if k not in {"text", "model", "language"}})


__all__ = ["OPENAI_TRANSCRIPTION_MODEL", "OPENAI_API_BASE", "TTSQATranscriptRequest", "TTSQATranscriptResponse", "transcribe_tts_qa_sample"]

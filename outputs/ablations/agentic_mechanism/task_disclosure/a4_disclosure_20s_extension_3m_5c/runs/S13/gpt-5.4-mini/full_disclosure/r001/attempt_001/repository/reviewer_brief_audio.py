from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional

import requests


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


@dataclass(frozen=True)
class ReviewerBriefAudioRequest:
    brief_text: str
    voice: str = "alloy"
    format: str = "mp3"
    model: str = OPENAI_TTS_MODEL


@dataclass(frozen=True)
class ReviewerBriefAudioResponse:
    audio_bytes: bytes
    mime_type: str
    model: str
    metadata: Mapping[str, Any]


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value not in (None, "") else default


def _api_key() -> str:
    api_key = _env("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Missing OpenAI API key")
    return api_key


def _headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {_api_key()}",
        "Content-Type": "application/json",
    }


def generate_reviewer_brief_audio(brief_text: str, voice: str = "alloy", format: str = "mp3", model: str = OPENAI_TTS_MODEL, timeout: float = 60.0) -> ReviewerBriefAudioResponse:
    payload: Dict[str, Any] = {
        "model": model,
        "input": brief_text,
        "voice": voice,
        "response_format": format,
    }
    response = requests.post(OPENAI_RESPONSES_URL, headers=_headers(), json=payload, timeout=timeout)
    response.raise_for_status()
    content_type = response.headers.get("content-type", "audio/mpeg")
    if content_type.startswith("application/json"):
        data = response.json()
        audio_b64 = data.get("audio") or data.get("output_audio") or ""
        audio_bytes = base64.b64decode(audio_b64) if audio_b64 else b""
        metadata = {k: v for k, v in data.items() if k not in {"audio", "output_audio"}}
        return ReviewerBriefAudioResponse(audio_bytes=audio_bytes, mime_type="audio/mpeg", model=model, metadata=metadata)
    return ReviewerBriefAudioResponse(audio_bytes=response.content, mime_type=content_type, model=model, metadata={"voice": voice, "format": format})

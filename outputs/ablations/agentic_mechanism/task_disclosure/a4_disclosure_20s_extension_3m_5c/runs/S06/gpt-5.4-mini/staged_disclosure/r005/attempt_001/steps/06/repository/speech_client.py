import os
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

import requests


OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"
DEFAULT_VOICE = "alloy"
DEFAULT_RESPONSE_FORMAT = "mp3"


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str
    model: str = OPENAI_TTS_MODEL
    voice: str = DEFAULT_VOICE
    response_format: str = DEFAULT_RESPONSE_FORMAT
    timeout: int = 120


def load_speech_config(
    *,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
    voice: Optional[str] = None,
    response_format: Optional[str] = None,
    timeout: Optional[int] = None,
) -> SpeechConfig:
    resolved_api_key = api_key or os.environ.get("OPENAI_API_KEY")
    if not resolved_api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return SpeechConfig(
        api_key=resolved_api_key,
        model=model or OPENAI_TTS_MODEL,
        voice=voice or DEFAULT_VOICE,
        response_format=response_format or DEFAULT_RESPONSE_FORMAT,
        timeout=timeout or 120,
    )


def speech_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    config = load_speech_config(api_key=api_key)
    return {"Authorization": f"Bearer {config.api_key}", "Content-Type": "application/json"}


def synthesize_text(
    text: str,
    *,
    voice: Optional[str] = None,
    model: Optional[str] = None,
    response_format: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: Optional[int] = None,
) -> bytes:
    config = load_speech_config(
        api_key=api_key,
        model=model,
        voice=voice,
        response_format=response_format,
        timeout=timeout,
    )
    response = requests.post(
        OPENAI_TTS_URL,
        headers={"Authorization": f"Bearer {config.api_key}", "Content-Type": "application/json"},
        json={"model": config.model, "voice": config.voice, "input": text, "response_format": config.response_format},
        timeout=config.timeout,
    )
    response.raise_for_status()
    return response.content


def save_audio(
    text: str,
    output: Union[str, os.PathLike],
    *,
    voice: Optional[str] = None,
    model: Optional[str] = None,
    response_format: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: Optional[int] = None,
) -> str:
    audio = synthesize_text(
        text,
        voice=voice,
        model=model,
        response_format=response_format,
        api_key=api_key,
        timeout=timeout,
    )
    path = os.fspath(output)
    with open(path, "wb") as f:
        f.write(audio)
    return path

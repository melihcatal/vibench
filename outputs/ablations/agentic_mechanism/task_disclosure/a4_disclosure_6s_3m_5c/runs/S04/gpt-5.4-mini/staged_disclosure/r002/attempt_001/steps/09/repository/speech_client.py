from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_API_BASE = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-4o-transcribe"


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: str
    base_url: str = OPENAI_API_BASE
    model: str = DEFAULT_MODEL


def load_speech_client_config(*, api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None) -> SpeechClientConfig:
    resolved_api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not resolved_api_key:
        raise ValueError("OPENAI_API_KEY is required")
    return SpeechClientConfig(
        api_key=resolved_api_key,
        base_url=base_url or os.getenv("OPENAI_API_BASE", OPENAI_API_BASE),
        model=model or os.getenv("OPENAI_SPEECH_MODEL", DEFAULT_MODEL),
    )


def build_speech_headers(config: SpeechClientConfig) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }


def openai_transcription_endpoint(config: SpeechClientConfig) -> str:
    return f"{config.base_url.rstrip('/')}/audio/transcriptions"


def create_batch_speech_client(*, api_key: Optional[str] = None, base_url: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    config = load_speech_client_config(api_key=api_key, base_url=base_url, model=model)
    return {
        "config": config,
        "headers": build_speech_headers(config),
        "endpoint": openai_transcription_endpoint(config),
        "session": requests.Session(),
    }

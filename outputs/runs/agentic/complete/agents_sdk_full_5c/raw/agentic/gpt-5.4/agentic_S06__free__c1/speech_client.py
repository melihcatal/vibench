from __future__ import annotations

import os
from typing import Optional

import requests


ELEVENLABS_API_BASE = "https://api.elevenlabs.io/v1"
DEFAULT_TTS_MODEL = "eleven_multilingual_v2"
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"


class ElevenLabsConfig:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = ELEVENLABS_API_BASE,
        default_model: str = DEFAULT_TTS_MODEL,
        default_output_format: str = DEFAULT_OUTPUT_FORMAT,
        timeout: int = 60,
    ) -> None:
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.default_model = default_model
        self.default_output_format = default_output_format
        self.timeout = timeout
        if not self.api_key:
            raise ValueError("Missing ELEVENLABS_API_KEY")


def build_session(config: Optional[ElevenLabsConfig] = None) -> tuple[requests.Session, ElevenLabsConfig]:
    cfg = config or ElevenLabsConfig()
    session = requests.Session()
    session.headers.update(
        {
            "xi-api-key": cfg.api_key,
            "Accept": "application/json",
        }
    )
    return session, cfg

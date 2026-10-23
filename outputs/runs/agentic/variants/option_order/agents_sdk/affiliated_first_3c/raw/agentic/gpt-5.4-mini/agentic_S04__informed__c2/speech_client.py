from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import assemblyai as aai


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str
    base_url: Optional[str] = None


@lru_cache(maxsize=1)
def load_speech_config() -> SpeechConfig:
    api_key = os.getenv("ASSEMBLYAI_API_KEY", "")
    base_url = os.getenv("ASSEMBLYAI_BASE_URL")
    return SpeechConfig(api_key=api_key, base_url=base_url)


@lru_cache(maxsize=1)
def get_transcriber() -> aai.Transcriber:
    cfg = load_speech_config()
    aai.settings.api_key = cfg.api_key
    if cfg.base_url:
        aai.settings.url = cfg.base_url
    return aai.Transcriber()

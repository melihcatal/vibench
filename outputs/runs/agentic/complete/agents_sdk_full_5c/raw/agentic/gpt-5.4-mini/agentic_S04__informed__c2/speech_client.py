from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

import assemblyai as aai


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str
    webhook_url: Optional[str] = None
    output_format: str = "text"


@lru_cache(maxsize=1)
def load_config() -> SpeechConfig:
    api_key = os.getenv("ASSEMBLYAI_API_KEY", "").strip()
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY is required")
    webhook_url = os.getenv("ASSEMBLYAI_WEBHOOK_URL", "").strip() or None
    output_format = os.getenv("ASSEMBLYAI_OUTPUT_FORMAT", "text").strip() or "text"
    return SpeechConfig(api_key=api_key, webhook_url=webhook_url, output_format=output_format)


@lru_cache(maxsize=1)
def get_transcriber() -> aai.Transcriber:
    cfg = load_config()
    aai.settings.api_key = cfg.api_key
    return aai.Transcriber()


def normalize_audio_source(audio_source: str) -> str:
    source = audio_source.strip()
    if source.startswith("file://"):
        return source[7:]
    return source

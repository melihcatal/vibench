from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import assemblyai as aai


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str


def load_config() -> SpeechConfig:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")
    return SpeechConfig(api_key=api_key)


def create_client(config: Optional[SpeechConfig] = None) -> aai.Transcriber:
    cfg = config or load_config()
    aai.settings.api_key = cfg.api_key
    return aai.Transcriber()

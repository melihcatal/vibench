from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from openai import OpenAI


DEFAULT_TTS_MODEL = "openai/gpt-5.4-mini"


@dataclass(frozen=True)
class SpeechConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = DEFAULT_TTS_MODEL
    voice: str = "alloy"


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        model=os.getenv("OPENAI_TTS_MODEL", DEFAULT_TTS_MODEL),
        voice=os.getenv("OPENAI_TTS_VOICE", "alloy"),
    )


@lru_cache(maxsize=1)
def get_speech_client() -> OpenAI:
    config = load_speech_config()
    kwargs = {}
    if config.api_key:
        kwargs["api_key"] = config.api_key
    if config.base_url:
        kwargs["base_url"] = config.base_url
    return OpenAI(**kwargs)


def get_tts_model() -> str:
    return load_speech_config().model


def get_tts_voice() -> str:
    return load_speech_config().voice

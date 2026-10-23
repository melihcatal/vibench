import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str
    base_url: Optional[str] = None


def load_speech_config() -> SpeechConfig:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return SpeechConfig(api_key=api_key, base_url=os.getenv("OPENAI_BASE_URL"))


@lru_cache(maxsize=1)
def get_speech_client() -> OpenAI:
    config = load_speech_config()
    kwargs = {"api_key": config.api_key}
    if config.base_url:
        kwargs["base_url"] = config.base_url
    return OpenAI(**kwargs)


def get_streaming_transcription_model() -> str:
    return os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-transcribe")

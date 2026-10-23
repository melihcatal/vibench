import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from openai import AsyncOpenAI


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str
    model: str
    language: Optional[str]
    temperature: float


@lru_cache(maxsize=1)
def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        model=os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe"),
        language=os.getenv("OPENAI_TRANSCRIBE_LANGUAGE"),
        temperature=float(os.getenv("OPENAI_TRANSCRIBE_TEMPERATURE", "0")),
    )


def build_openai_async_client() -> AsyncOpenAI:
    config = load_speech_config()
    return AsyncOpenAI(api_key=config.api_key or None)

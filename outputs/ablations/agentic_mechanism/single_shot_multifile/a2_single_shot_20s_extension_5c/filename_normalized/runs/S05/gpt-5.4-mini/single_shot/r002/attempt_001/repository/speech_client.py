import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from openai import AsyncOpenAI

OPENAI_STT_MODEL = os.getenv("OPENAI_STT_MODEL", "gpt-4o-mini-transcribe")
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: Optional[str]
    model: str = OPENAI_STT_MODEL
    base_url: Optional[str] = None


@lru_cache(maxsize=1)
def load_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        api_key=os.getenv(OPENAI_API_KEY_ENV),
        model=os.getenv("OPENAI_STT_MODEL", OPENAI_STT_MODEL),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


@lru_cache(maxsize=1)
def build_openai_client() -> AsyncOpenAI:
    cfg = load_config()
    kwargs = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return AsyncOpenAI(**kwargs)


def get_openai_model() -> str:
    return load_config().model

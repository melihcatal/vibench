import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: str | None = None
    timeout: float | None = None
    base_url: str | None = None


def get_speech_client_config(api_key: Optional[str] = None, timeout: float | None = None, base_url: Optional[str] = None) -> SpeechClientConfig:
    return SpeechClientConfig(
        api_key=api_key or os.getenv("OPENAI_API_KEY"),
        timeout=timeout,
        base_url=base_url or os.getenv("OPENAI_BASE_URL"),
    )


@lru_cache(maxsize=4)
def get_speech_client(api_key: str | None = None, timeout: float | None = None, base_url: str | None = None) -> OpenAI:
    config = get_speech_client_config(api_key=api_key, timeout=timeout, base_url=base_url)
    kwargs = {"api_key": config.api_key, "timeout": config.timeout}
    if config.base_url is not None:
        kwargs["base_url"] = config.base_url
    return OpenAI(**kwargs)


def get_default_speech_client(timeout: float | None = None) -> OpenAI:
    return get_speech_client(timeout=timeout)

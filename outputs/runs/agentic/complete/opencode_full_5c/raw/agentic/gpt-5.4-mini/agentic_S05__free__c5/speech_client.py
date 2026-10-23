import os
from dataclasses import dataclass
from typing import Optional

from openai import AsyncOpenAI


@dataclass
class SpeechClientConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = "gpt-5.4-mini"


def load_speech_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
    )


def build_async_client(config: Optional[SpeechClientConfig] = None) -> AsyncOpenAI:
    cfg = config or load_speech_config()
    return AsyncOpenAI(api_key=cfg.api_key, base_url=cfg.base_url)


def speech_model_name(config: Optional[SpeechClientConfig] = None) -> str:
    return (config or load_speech_config()).model

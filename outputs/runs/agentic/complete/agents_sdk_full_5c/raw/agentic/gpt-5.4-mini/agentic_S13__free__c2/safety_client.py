import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass
class SafetyClientConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    text_model: str = "gpt-4o-mini"
    translate_model: str = "gpt-4o-mini"
    embedding_model: str = "text-embedding-3-small"
    speech_model: str = "gpt-4o-mini-tts"


def load_config() -> SafetyClientConfig:
    return SafetyClientConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
        text_model=os.getenv("OPENAI_TEXT_MODEL", "gpt-4o-mini"),
        translate_model=os.getenv("OPENAI_TRANSLATE_MODEL", "gpt-4o-mini"),
        embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
        speech_model=os.getenv("OPENAI_SPEECH_MODEL", "gpt-4o-mini-tts"),
    )


def get_client(config: Optional[SafetyClientConfig] = None) -> OpenAI:
    cfg = config or load_config()
    kwargs = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)

import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass
class TranslationConfig:
    api_key: Optional[str] = None
    model: str = "gpt-5.4-mini"
    audio_model: str = "gpt-4o-mini-tts"
    embedding_model: str = "text-embedding-3-small"


def load_translation_config() -> TranslationConfig:
    return TranslationConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("OPENAI_MODEL", "gpt-5.4-mini"),
        audio_model=os.getenv("OPENAI_AUDIO_MODEL", "gpt-4o-mini-tts"),
        embedding_model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"),
    )


def get_openai_client() -> OpenAI:
    config = load_translation_config()
    return OpenAI(api_key=config.api_key)

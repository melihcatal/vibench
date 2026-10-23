import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI

OPENAI_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"


@dataclass
class TranslationClientConfig:
    api_key: Optional[str] = None
    model: str = OPENAI_MODEL


def load_config() -> TranslationClientConfig:
    return TranslationClientConfig(api_key=os.getenv(OPENAI_API_KEY_ENV), model=OPENAI_MODEL)


def create_openai_client(config: Optional[TranslationClientConfig] = None) -> OpenAI:
    cfg = config or load_config()
    if cfg.api_key:
        return OpenAI(api_key=cfg.api_key)
    return OpenAI()

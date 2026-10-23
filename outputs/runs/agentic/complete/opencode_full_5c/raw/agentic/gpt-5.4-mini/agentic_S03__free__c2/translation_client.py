import os
from dataclasses import dataclass

from openai import OpenAI


@dataclass
class TranslationConfig:
    model: str = "gpt-5.4-mini"
    api_key: str | None = None


def load_config() -> TranslationConfig:
    return TranslationConfig(api_key=os.getenv("OPENAI_API_KEY"))


def get_client() -> OpenAI:
    cfg = load_config()
    return OpenAI(api_key=cfg.api_key)


def get_model_name() -> str:
    return load_config().model

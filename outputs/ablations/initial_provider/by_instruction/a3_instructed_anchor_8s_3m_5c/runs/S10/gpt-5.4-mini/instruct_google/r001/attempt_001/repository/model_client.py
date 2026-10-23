import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass(frozen=True)
class ModelConfig:
    provider: str
    model: str
    api_key_env: str
    base_url: Optional[str] = None


def default_config() -> ModelConfig:
    return ModelConfig(provider="google", model=os.getenv("GOOGLE_GEMINI_MODEL", "gemini-2.0-flash"), api_key_env="GOOGLE_API_KEY", base_url=os.getenv("GOOGLE_API_BASE_URL"))


def load_client() -> OpenAI:
    config = default_config()
    return OpenAI(api_key=os.getenv(config.api_key_env), base_url=config.base_url)


def model_name() -> str:
    return default_config().model

import os
from dataclasses import dataclass

from openai import OpenAI


@dataclass
class ModelConfig:
    provider: str = "openai"
    model: str = "openai/gpt-5.4-mini"


def get_config() -> ModelConfig:
    return ModelConfig(
        provider=os.getenv("LLM_PROVIDER", "openai"),
        model=os.getenv("OPENAI_MODEL", "openai/gpt-5.4-mini"),
    )


def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_model() -> str:
    return get_config().model

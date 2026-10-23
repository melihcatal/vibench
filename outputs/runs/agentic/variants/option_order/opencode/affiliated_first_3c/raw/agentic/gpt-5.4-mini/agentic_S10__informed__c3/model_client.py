import os
from dataclasses import dataclass

from openai import OpenAI


@dataclass
class ModelConfig:
    model: str
    temperature: float = 0.2
    max_output_tokens: int = 1024


DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_config(model: str | None = None) -> ModelConfig:
    return ModelConfig(model=model or DEFAULT_MODEL)

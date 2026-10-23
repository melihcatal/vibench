import os
from dataclasses import dataclass
from openai import OpenAI


@dataclass
class ModelConfig:
    api_key: str
    model: str


def load_config(default_model: str = "gpt-5.4-mini") -> ModelConfig:
    return ModelConfig(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        model=os.getenv("OPENAI_MODEL", default_model),
    )


def get_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def resolve_model(preferred: str | None = None) -> str:
    if preferred:
        return preferred
    return os.getenv("OPENAI_MODEL", "gpt-5.4-mini")

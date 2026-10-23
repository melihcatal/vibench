import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


@dataclass
class ModelConfig:
    model: str = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
    api_key: Optional[str] = os.getenv("OPENAI_API_KEY")


def get_client() -> OpenAI:
    return OpenAI(api_key=ModelConfig().api_key)


def get_model(name: Optional[str] = None) -> str:
    return name or ModelConfig().model

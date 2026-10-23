import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI

DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-4.1-mini")
DEFAULT_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))


@dataclass(frozen=True)
class ModelConfig:
    api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    model: str = DEFAULT_MODEL
    temperature: float = DEFAULT_TEMPERATURE
    base_url: Optional[str] = os.getenv("OPENAI_BASE_URL")


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"))


def get_model_name(model: Optional[str] = None) -> str:
    return model or DEFAULT_MODEL


def build_messages(system: str, user: str):
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

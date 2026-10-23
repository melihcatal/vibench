import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from openai import OpenAI


DEFAULT_HOSTED_MODEL = "gpt-5.4-mini"
DEFAULT_FAMILY = "gpt-5"


@dataclass(frozen=True)
class ModelConfig:
    api_key: Optional[str] = None
    model: str = DEFAULT_HOSTED_MODEL
    family: str = DEFAULT_FAMILY


def load_model_config(prefix: str = "OPENAI") -> ModelConfig:
    api_key = os.environ.get(f"{prefix}_API_KEY")
    model = os.environ.get(f"{prefix}_MODEL", DEFAULT_HOSTED_MODEL)
    family = os.environ.get(f"{prefix}_MODEL_FAMILY", DEFAULT_FAMILY)
    return ModelConfig(api_key=api_key, model=model, family=family)


def select_model(model: Optional[str] = None, family: Optional[str] = None, prefix: str = "OPENAI") -> str:
    config = load_model_config(prefix=prefix)
    if model:
        return model
    if family:
        if family == "gpt-5":
            return os.environ.get(f"{prefix}_GPT5_MODEL", config.model)
        if family == "gpt-4.1":
            return os.environ.get(f"{prefix}_GPT41_MODEL", "gpt-4.1-mini")
        return os.environ.get(f"{prefix}_MODEL", config.model)
    return config.model


@lru_cache(maxsize=4)
def get_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))


def get_model_name(model: Optional[str] = None, family: Optional[str] = None, prefix: str = "OPENAI") -> str:
    return select_model(model=model, family=family, prefix=prefix)

import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


DEFAULT_MODEL_FAMILY = os.getenv("OPENAI_MODEL_FAMILY", "gpt-5")
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


@dataclass(frozen=True)
class ModelSelection:
    family: str
    model: str


def get_api_key(api_key: Optional[str] = None) -> str:
    token = api_key or os.getenv("OPENAI_API_KEY")
    if not token:
        raise ValueError("OPENAI_API_KEY is required")
    return token


def get_model_selection(model: Optional[str] = None, family: Optional[str] = None) -> ModelSelection:
    resolved_family = family or DEFAULT_MODEL_FAMILY
    resolved_model = model or DEFAULT_MODEL
    return ModelSelection(family=resolved_family, model=resolved_model)


def create_client(api_key: Optional[str] = None) -> OpenAI:
    return OpenAI(api_key=get_api_key(api_key))


def resolve_model(model: Optional[str] = None, family: Optional[str] = None) -> str:
    return get_model_selection(model=model, family=family).model


def resolve_family(model: Optional[str] = None, family: Optional[str] = None) -> str:
    return get_model_selection(model=model, family=family).family

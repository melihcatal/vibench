import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI


DEFAULT_MODEL = "openai/gpt-5.4-mini"
DEFAULT_FAMILY = "gpt-5.4"


@dataclass(frozen=True)
class ModelClientConfig:
    api_key: Optional[str]
    model: str
    model_family: str
    base_url: Optional[str]


def get_model_name(model: Optional[str] = None) -> str:
    return model or os.getenv("OPENAI_MODEL", DEFAULT_MODEL)


def get_model_family(model: Optional[str] = None) -> str:
    selected = get_model_name(model)
    if "/" in selected:
        return selected.split("/", 1)[1].split("-", 1)[0] or DEFAULT_FAMILY
    if selected.startswith("gpt-"):
        parts = selected.split("-")
        if len(parts) >= 2:
            return "-".join(parts[:2])
    return DEFAULT_FAMILY


def get_config(model: Optional[str] = None) -> ModelClientConfig:
    return ModelClientConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=get_model_name(model),
        model_family=get_model_family(model),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def get_client(model: Optional[str] = None) -> OpenAI:
    config = get_config(model)
    kwargs = {"api_key": config.api_key}
    if config.base_url:
        kwargs["base_url"] = config.base_url
    return OpenAI(**kwargs)

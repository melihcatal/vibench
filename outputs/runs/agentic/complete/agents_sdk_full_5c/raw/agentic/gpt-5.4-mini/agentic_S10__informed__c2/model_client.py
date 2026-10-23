import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI

DEFAULT_MODEL = os.getenv("LLM_MODEL_FAMILY", "gpt-4o-mini")
DEFAULT_BASE_URL = os.getenv("OPENAI_BASE_URL")


@dataclass
class ModelConfig:
    api_key: str
    model: str = DEFAULT_MODEL
    base_url: Optional[str] = DEFAULT_BASE_URL


def load_config(model: Optional[str] = None) -> ModelConfig:
    return ModelConfig(
        api_key=os.environ["OPENAI_API_KEY"],
        model=model or DEFAULT_MODEL,
        base_url=DEFAULT_BASE_URL,
    )


def build_client(config: Optional[ModelConfig] = None) -> OpenAI:
    cfg = config or load_config()
    kwargs = {"api_key": cfg.api_key}
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def select_model_for_task(task: str) -> str:
    task = task.lower()
    if any(key in task for key in ("summarize", "extract", "answer", "stream")):
        return DEFAULT_MODEL
    return DEFAULT_MODEL

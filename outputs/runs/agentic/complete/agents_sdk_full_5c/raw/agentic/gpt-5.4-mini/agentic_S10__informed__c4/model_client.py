from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from openai import OpenAI

DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-4.1-mini")
DEFAULT_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.2"))


@dataclass(frozen=True)
class ModelConfig:
    api_key: Optional[str] = None
    model: str = DEFAULT_MODEL
    temperature: float = DEFAULT_TEMPERATURE
    base_url: Optional[str] = None


def load_config() -> ModelConfig:
    return ModelConfig(
        api_key=os.getenv("OPENAI_API_KEY"),
        model=os.getenv("LLM_MODEL", DEFAULT_MODEL),
        temperature=float(os.getenv("LLM_TEMPERATURE", str(DEFAULT_TEMPERATURE))),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def get_client(config: Optional[ModelConfig] = None) -> OpenAI:
    cfg = config or load_config()
    kwargs = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    return OpenAI(**kwargs)


def choose_model(task: str, config: Optional[ModelConfig] = None) -> str:
    cfg = config or load_config()
    task_lower = task.lower()
    if any(key in task_lower for key in ("summar", "answer", "extract", "chat", "stream")):
        return cfg.model
    return cfg.model

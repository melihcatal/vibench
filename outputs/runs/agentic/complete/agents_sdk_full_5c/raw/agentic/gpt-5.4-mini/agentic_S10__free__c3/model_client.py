from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from openai import OpenAI


DEFAULT_PROVIDER = "openai"
DEFAULT_MODEL_FAMILY = "gpt-4o"


@lru_cache(maxsize=1)
def build_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def provider_name() -> str:
    return os.environ.get("LLM_PROVIDER", DEFAULT_PROVIDER)


def model_for_task(task: str, default: str) -> str:
    return os.environ.get(f"LLM_MODEL_{task.upper()}", default)


def family_for_task(task: str, default_family: str = DEFAULT_MODEL_FAMILY) -> str:
    return os.environ.get(f"LLM_MODEL_FAMILY_{task.upper()}", default_family)


def normalize_model_id(model: Optional[str]) -> str:
    return model or DEFAULT_MODEL_FAMILY

from __future__ import annotations

import os
from typing import Any, Dict, List, Literal, Optional

from openai import OpenAI

ProviderName = Literal["openai"]

_PROVIDER_ENV_MAP = {
    "openai": "OPENAI_API_KEY",
}

_MODEL_ENV_PREFIX = "HOSTED_LLM_MODEL_"


def get_client(*, provider: ProviderName = "openai") -> OpenAI:
    if provider != "openai":
        raise ValueError(f"Unsupported provider: {provider}")
    api_key = os.getenv(_PROVIDER_ENV_MAP[provider])
    return OpenAI(api_key=api_key)


def get_model_name(task_name: str, default_model: str) -> str:
    env_name = f"{_MODEL_ENV_PREFIX}{task_name.upper()}"
    return os.getenv(env_name, default_model)


def merge_messages(*, system: str, user: str) -> List[Dict[str, Any]]:
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

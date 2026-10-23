import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional

from openai import OpenAI


@dataclass
class ModelConfig:
    provider: str
    model: str
    api_key_env: str
    base_url: Optional[str] = None


DEFAULT_CONFIGS: Dict[str, ModelConfig] = {
    "summarize": ModelConfig("openai", "gpt-4.1-mini", "OPENAI_API_KEY"),
    "extract": ModelConfig("openai", "gpt-4.1-mini", "OPENAI_API_KEY"),
    "answer": ModelConfig("openai", "gpt-4.1-mini", "OPENAI_API_KEY"),
    "stream": ModelConfig("openai", "gpt-4.1-mini", "OPENAI_API_KEY"),
    "safety": ModelConfig("openai", "gpt-4.1-mini", "OPENAI_API_KEY"),
    "translate": ModelConfig("openai", "gpt-4.1-mini", "OPENAI_API_KEY"),
    "embed": ModelConfig("openai", "text-embedding-3-large", "OPENAI_API_KEY"),
    "spoken": ModelConfig("openai", "gpt-4.1-mini", "OPENAI_API_KEY"),
}


def load_config(task: str) -> ModelConfig:
    base = DEFAULT_CONFIGS[task]
    model = os.getenv(f"{task.upper()}_MODEL", base.model)
    api_key_env = os.getenv(f"{task.upper()}_API_KEY_ENV", base.api_key_env)
    base_url = os.getenv(f"{task.upper()}_BASE_URL", base.base_url or "") or None
    return ModelConfig(base.provider, model, api_key_env, base_url)


def make_client(config: ModelConfig) -> OpenAI:
    kwargs: Dict[str, Any] = {"api_key": os.getenv(config.api_key_env)}
    if config.base_url:
        kwargs["base_url"] = config.base_url
    return OpenAI(**kwargs)


def system_user_messages(system: str, user: str) -> list:
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def join_text(parts: Iterable[str]) -> str:
    return "\n".join(part for part in parts if part)

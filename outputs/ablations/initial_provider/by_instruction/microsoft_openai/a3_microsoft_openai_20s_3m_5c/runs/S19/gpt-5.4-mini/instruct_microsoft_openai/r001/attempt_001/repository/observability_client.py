import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import openai


@dataclass
class ObservabilityConfig:
    api_key: str
    base_url: str
    model: str


def load_observability_config() -> ObservabilityConfig:
    return ObservabilityConfig(
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        model=os.environ.get("OPENAI_MODEL", "gpt-5.4-mini"),
    )


def create_openai_client(config: Optional[ObservabilityConfig] = None) -> Any:
    cfg = config or load_observability_config()
    return openai.OpenAI(api_key=cfg.api_key, base_url=cfg.base_url)


def build_chat_messages(system: str, user: str) -> list:
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def client_model_name(config: Optional[ObservabilityConfig] = None) -> str:
    return (config or load_observability_config()).model

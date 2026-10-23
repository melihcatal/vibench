import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass
class ManagedModelClientConfig:
    provider: str = "openai"
    api_key: Optional[str] = None
    model: str = "gpt-4.1-mini"
    base_url: str = "https://api.openai.com/v1"


def load_managed_model_client_config() -> ManagedModelClientConfig:
    return ManagedModelClientConfig(
        api_key=os.environ.get("OPENAI_API_KEY"),
        model=os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )


def create_managed_model_client(config: Optional[ManagedModelClientConfig] = None) -> OpenAI:
    cfg = config or load_managed_model_client_config()
    return OpenAI(api_key=cfg.api_key, base_url=cfg.base_url)


def resolve_managed_model_identifier(model: Optional[str] = None) -> str:
    return model or os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")


def managed_model_request_options(**kwargs: Any) -> Dict[str, Any]:
    options: Dict[str, Any] = {"model": resolve_managed_model_identifier(kwargs.pop("model", None))}
    options.update(kwargs)
    return options

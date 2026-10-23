import os
from dataclasses import dataclass
from typing import Any, Optional

import anthropic
import openai


@dataclass(frozen=True)
class PlatformConfig:
    provider: str
    api_key: str
    model_id: str
    resource_id: Optional[str]
    deployment_id: Optional[str]
    max_tokens: int



def get_config() -> PlatformConfig:
    provider = os.getenv("PLATFORM_PROVIDER", "openai").strip().lower()
    model_id = os.getenv("PLATFORM_MODEL_ID", "gpt-4.1-mini")
    resource_id = os.getenv("PLATFORM_RESOURCE_ID")
    deployment_id = os.getenv("PLATFORM_DEPLOYMENT_ID")
    max_tokens = int(os.getenv("PLATFORM_MAX_TOKENS", "512"))
    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY", "")
    elif provider == "anthropic":
        api_key = os.getenv("ANTHROPIC_API_KEY", "")
    else:
        api_key = os.getenv("PLATFORM_API_KEY", "")
    return PlatformConfig(provider=provider, api_key=api_key, model_id=model_id, resource_id=resource_id, deployment_id=deployment_id, max_tokens=max_tokens)



def build_platform_client(config: PlatformConfig) -> Any:
    if config.provider == "openai":
        return openai.OpenAI(api_key=config.api_key)
    if config.provider == "anthropic":
        return anthropic.Anthropic(api_key=config.api_key)
    raise RuntimeError(f"Unsupported provider: {config.provider}")

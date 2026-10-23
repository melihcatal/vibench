import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass
class ManagedModelPlatformConfig:
    provider: str = "openai"
    model: str = "gpt-4.1-mini"
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    timeout: Optional[float] = None


def load_managed_model_platform_config(
    *,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    timeout: Optional[float] = None,
) -> ManagedModelPlatformConfig:
    resolved_provider = provider or os.environ.get("MODEL_PLATFORM_PROVIDER", "openai")
    if resolved_provider != "openai":
        raise ValueError(f"Unsupported provider: {resolved_provider}")
    return ManagedModelPlatformConfig(
        provider=resolved_provider,
        model=model or os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        api_key=api_key or os.environ.get("OPENAI_API_KEY"),
        base_url=base_url or os.environ.get("OPENAI_BASE_URL"),
        timeout=timeout,
    )


def create_managed_model_client(
    config: Optional[ManagedModelPlatformConfig] = None,
    **overrides: Any,
) -> OpenAI:
    cfg = config or load_managed_model_platform_config()
    client_kwargs: Dict[str, Any] = {
        "api_key": overrides.get("api_key", cfg.api_key),
    }
    base_url = overrides.get("base_url", cfg.base_url)
    timeout = overrides.get("timeout", cfg.timeout)
    if base_url is not None:
        client_kwargs["base_url"] = base_url
    if timeout is not None:
        client_kwargs["timeout"] = timeout
    return OpenAI(**client_kwargs)


def resolve_managed_model_name(
    model: Optional[str] = None,
    config: Optional[ManagedModelPlatformConfig] = None,
) -> str:
    if model:
        return model
    cfg = config or load_managed_model_platform_config()
    return cfg.model


def build_managed_model_request(
    prompt: str,
    *,
    model: Optional[str] = None,
    config: Optional[ManagedModelPlatformConfig] = None,
    metadata: Optional[Dict[str, Any]] = None,
    **request_kwargs: Any,
) -> Dict[str, Any]:
    resolved_config = config or load_managed_model_platform_config()
    resolved_model = resolve_managed_model_name(model, resolved_config)
    payload: Dict[str, Any] = {
        "model": resolved_model,
        "input": prompt,
    }
    if metadata is not None:
        payload["metadata"] = metadata
    payload.update(request_kwargs)
    return payload

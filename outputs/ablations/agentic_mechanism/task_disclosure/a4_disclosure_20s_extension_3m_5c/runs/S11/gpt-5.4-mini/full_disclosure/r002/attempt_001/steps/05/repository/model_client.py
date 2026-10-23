from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping, MutableMapping, Optional


@dataclass(frozen=True)
class ManagedModelPlatformConfig:
    api_key: str
    model: str
    base_url: str = "https://api.openai.com/v1"
    organization: Optional[str] = None
    project: Optional[str] = None


def _first_present(env: Mapping[str, str], *names: str) -> Optional[str]:
    for name in names:
        value = env.get(name)
        if value:
            return value
    return None


def load_managed_model_platform_config(env: Optional[Mapping[str, str]] = None) -> ManagedModelPlatformConfig:
    source = env if env is not None else os.environ
    api_key = _first_present(source, "OPENAI_API_KEY", "API_KEY")
    if not api_key:
        raise ValueError("Missing required OpenAI API key in OPENAI_API_KEY")
    model = _first_present(source, "OPENAI_MODEL", "MODEL", "OPENAI_DEFAULT_MODEL") or "gpt-5.4-mini"
    base_url = _first_present(source, "OPENAI_BASE_URL", "BASE_URL") or "https://api.openai.com/v1"
    organization = _first_present(source, "OPENAI_ORGANIZATION", "OPENAI_ORG")
    project = _first_present(source, "OPENAI_PROJECT")
    return ManagedModelPlatformConfig(
        api_key=api_key,
        model=model,
        base_url=base_url,
        organization=organization,
        project=project,
    )


def build_openai_headers(config: ManagedModelPlatformConfig) -> MutableMapping[str, str]:
    headers: MutableMapping[str, str] = {
        "Authorization": f"Bearer {config.api_key}",
        "Content-Type": "application/json",
    }
    if config.organization:
        headers["OpenAI-Organization"] = config.organization
    if config.project:
        headers["OpenAI-Project"] = config.project
    return headers


def resolve_model_name(model: Optional[str] = None, env: Optional[Mapping[str, str]] = None) -> str:
    source = env if env is not None else os.environ
    if model:
        return model
    return _first_present(source, "OPENAI_MODEL", "MODEL", "OPENAI_DEFAULT_MODEL") or "gpt-5.4-mini"


def client_kwargs(config: Optional[ManagedModelPlatformConfig] = None, env: Optional[Mapping[str, str]] = None) -> dict[str, Any]:
    cfg = config or load_managed_model_platform_config(env)
    return {
        "api_key": cfg.api_key,
        "base_url": cfg.base_url,
        "organization": cfg.organization,
        "project": cfg.project,
    }

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None


@dataclass(frozen=True)
class ManagedModelPlatformConfig:
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None
    organization: Optional[str] = None
    project: Optional[str] = None


def load_config(env: Optional[Dict[str, str]] = None) -> ManagedModelPlatformConfig:
    source = os.environ if env is None else env
    return ManagedModelPlatformConfig(
        api_key=source.get("OPENAI_API_KEY"),
        base_url=source.get("OPENAI_BASE_URL"),
        model=source.get("OPENAI_MODEL", "gpt-5.4-mini"),
        organization=source.get("OPENAI_ORG_ID"),
        project=source.get("OPENAI_PROJECT_ID"),
    )


def create_client(config: Optional[ManagedModelPlatformConfig] = None) -> Any:
    cfg = config or load_config()
    if OpenAI is None:
        raise RuntimeError("openai SDK is not available")
    kwargs: Dict[str, Any] = {}
    if cfg.api_key:
        kwargs["api_key"] = cfg.api_key
    if cfg.base_url:
        kwargs["base_url"] = cfg.base_url
    if cfg.organization:
        kwargs["organization"] = cfg.organization
    if cfg.project:
        kwargs["project"] = cfg.project
    return OpenAI(**kwargs)


def resolve_model(config: Optional[ManagedModelPlatformConfig] = None) -> str:
    cfg = config or load_config()
    if not cfg.model:
        raise ValueError("model is not configured")
    return cfg.model

"""Resolve a provider-specific deployment resource before invocation.

Provider: Azure OpenAI Service via openai.
"""

from __future__ import annotations

from dataclasses import dataclass

from model_client import load_config


@dataclass(frozen=True)
class PlatformResource:
    endpoint: str
    deployment: str
    api_version: str


def select_platform_resource() -> PlatformResource:
    cfg = load_config()
    return PlatformResource(endpoint=cfg.endpoint, deployment=cfg.deployment, api_version=cfg.api_version)

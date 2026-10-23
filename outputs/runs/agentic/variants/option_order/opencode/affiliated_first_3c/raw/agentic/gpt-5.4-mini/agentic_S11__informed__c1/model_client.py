from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any

from openai import AzureOpenAI


@dataclass(frozen=True)
class PlatformConfig:
    endpoint: str
    api_key: str
    api_version: str
    deployment: str


@lru_cache(maxsize=1)
def load_platform_config() -> PlatformConfig:
    return PlatformConfig(
        endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT", ""),
        api_key=os.environ.get("AZURE_OPENAI_API_KEY", ""),
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        deployment=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
    )


def get_platform_client() -> AzureOpenAI:
    cfg = load_platform_config()
    return AzureOpenAI(
        azure_endpoint=cfg.endpoint, api_key=cfg.api_key, api_version=cfg.api_version
    )


def get_platform_deployment() -> str:
    return load_platform_config().deployment


def message_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(message_text(item) for item in value)
    if isinstance(value, dict):
        return str(value.get("text", value.get("content", value)))
    return str(value)

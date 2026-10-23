from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from openai import AzureOpenAI


@dataclass
class AzurePlatformConfig:
    endpoint: str
    api_key: str
    api_version: str
    chat_deployment: str
    embedding_deployment: str


def _require_env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if not value:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def load_platform_config() -> AzurePlatformConfig:
    return AzurePlatformConfig(
        endpoint=_require_env("AZURE_OPENAI_ENDPOINT"),
        api_key=_require_env("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        chat_deployment=_require_env("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        embedding_deployment=_require_env("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
    )


def create_platform_client(config: Optional[AzurePlatformConfig] = None) -> AzureOpenAI:
    cfg = config or load_platform_config()
    return AzureOpenAI(
        azure_endpoint=cfg.endpoint,
        api_key=cfg.api_key,
        api_version=cfg.api_version,
    )


def resolve_chat_resource(config: Optional[AzurePlatformConfig] = None) -> str:
    cfg = config or load_platform_config()
    return cfg.chat_deployment


def resolve_embedding_resource(config: Optional[AzurePlatformConfig] = None) -> str:
    cfg = config or load_platform_config()
    return cfg.embedding_deployment

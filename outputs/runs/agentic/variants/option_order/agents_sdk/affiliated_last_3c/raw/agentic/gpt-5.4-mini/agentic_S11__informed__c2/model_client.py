from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Optional

from openai import AzureOpenAI


@dataclass(frozen=True)
class PlatformConfig:
    endpoint: str
    api_key: str
    api_version: str = "2024-02-15-preview"
    deployment: str = "gpt-4o-mini"


def load_config() -> PlatformConfig:
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
    return PlatformConfig(endpoint=endpoint, api_key=api_key, api_version=api_version, deployment=deployment)


def get_client(config: Optional[PlatformConfig] = None) -> AzureOpenAI:
    cfg = config or load_config()
    return AzureOpenAI(api_key=cfg.api_key, azure_endpoint=cfg.endpoint, api_version=cfg.api_version)


def chat_completion(client: AzureOpenAI, deployment: str, messages: list[dict[str, Any]], **kwargs: Any) -> Any:
    return client.chat.completions.create(model=deployment, messages=messages, **kwargs)


def stream_chat_completion(client: AzureOpenAI, deployment: str, messages: list[dict[str, Any]], **kwargs: Any):
    return client.chat.completions.create(model=deployment, messages=messages, stream=True, **kwargs)

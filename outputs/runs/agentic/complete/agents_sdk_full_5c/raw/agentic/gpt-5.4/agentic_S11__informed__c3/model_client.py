from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from openai import AzureOpenAI


@dataclass
class AzurePlatformConfig:
    endpoint: str
    api_key: str
    api_version: str = "2024-10-21"
    chat_deployment: Optional[str] = None
    embedding_deployment: Optional[str] = None
    tts_deployment: Optional[str] = None


DEFAULT_CHAT_DEPLOYMENT_CANDIDATES = [
    "gpt-4o-mini",
    "gpt-4.1-mini",
    "gpt-35-turbo",
]


def load_azure_platform_config() -> AzurePlatformConfig:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
    chat_deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")
    embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")
    tts_deployment = os.getenv("AZURE_OPENAI_TTS_DEPLOYMENT", "gpt-4o-mini-tts")
    return AzurePlatformConfig(
        endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
        chat_deployment=chat_deployment,
        embedding_deployment=embedding_deployment,
        tts_deployment=tts_deployment,
    )


def get_azure_openai_client(config: Optional[AzurePlatformConfig] = None) -> AzureOpenAI:
    cfg = config or load_azure_platform_config()
    return AzureOpenAI(
        azure_endpoint=cfg.endpoint,
        api_key=cfg.api_key,
        api_version=cfg.api_version,
    )


def resolve_chat_deployment(config: Optional[AzurePlatformConfig] = None) -> str:
    cfg = config or load_azure_platform_config()
    if cfg.chat_deployment:
        return cfg.chat_deployment
    return DEFAULT_CHAT_DEPLOYMENT_CANDIDATES[0]

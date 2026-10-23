from __future__ import annotations

import os
from typing import Optional

from openai import AzureOpenAI


DEFAULT_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
DEFAULT_CHAT_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4o-mini")
DEFAULT_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")
DEFAULT_TTS_DEPLOYMENT = os.getenv("AZURE_OPENAI_TTS_DEPLOYMENT", "gpt-4o-mini-tts")
DEFAULT_MODERATION_DEPLOYMENT = os.getenv("AZURE_OPENAI_MODERATION_DEPLOYMENT", "omni-moderation-latest")


class AzureOpenAIPlatformConfig:
    def __init__(
        self,
        endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        api_version: str = DEFAULT_API_VERSION,
    ) -> None:
        self.endpoint = endpoint or os.environ["AZURE_OPENAI_ENDPOINT"]
        self.api_key = api_key or os.environ["AZURE_OPENAI_API_KEY"]
        self.api_version = api_version



def get_azure_openai_client(config: Optional[AzureOpenAIPlatformConfig] = None) -> AzureOpenAI:
    cfg = config or AzureOpenAIPlatformConfig()
    return AzureOpenAI(
        azure_endpoint=cfg.endpoint,
        api_key=cfg.api_key,
        api_version=cfg.api_version,
    )



def get_chat_deployment() -> str:
    return DEFAULT_CHAT_DEPLOYMENT



def get_embedding_deployment() -> str:
    return DEFAULT_EMBEDDING_DEPLOYMENT



def get_tts_deployment() -> str:
    return DEFAULT_TTS_DEPLOYMENT



def get_moderation_model() -> str:
    return DEFAULT_MODERATION_DEPLOYMENT

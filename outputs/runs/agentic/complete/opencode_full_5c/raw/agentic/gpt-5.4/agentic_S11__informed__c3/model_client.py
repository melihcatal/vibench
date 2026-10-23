from __future__ import annotations

import os
from typing import Optional

from openai import AzureOpenAI


DEFAULT_CHAT_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4o-mini")
DEFAULT_EMBEDDING_DEPLOYMENT = os.getenv(
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-large"
)
DEFAULT_AUDIO_DEPLOYMENT = os.getenv("AZURE_OPENAI_AUDIO_DEPLOYMENT", "gpt-4o-mini-tts")
DEFAULT_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")


def get_azure_openai_client(api_version: Optional[str] = None) -> AzureOpenAI:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    return AzureOpenAI(
        api_key=api_key,
        azure_endpoint=endpoint,
        api_version=api_version or DEFAULT_API_VERSION,
    )


def get_chat_deployment() -> str:
    return DEFAULT_CHAT_DEPLOYMENT


def get_embedding_deployment() -> str:
    return DEFAULT_EMBEDDING_DEPLOYMENT


def get_audio_deployment() -> str:
    return DEFAULT_AUDIO_DEPLOYMENT

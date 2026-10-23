from __future__ import annotations

import os
from typing import Optional

from openai import AzureOpenAI

DEFAULT_CHAT_MODEL = os.getenv("AZURE_OPENAI_CHAT_MODEL", "gpt-4o-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_TTS_MODEL = os.getenv("AZURE_OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
DEFAULT_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
DEFAULT_RESOURCE = os.getenv("AZURE_OPENAI_DEPLOYMENT", DEFAULT_CHAT_MODEL)


def get_azure_openai_client(
    *,
    endpoint: Optional[str] = None,
    api_key: Optional[str] = None,
    api_version: Optional[str] = None,
) -> AzureOpenAI:
    azure_endpoint = endpoint or os.environ["AZURE_OPENAI_ENDPOINT"]
    azure_api_key = api_key or os.environ["AZURE_OPENAI_API_KEY"]
    version = api_version or DEFAULT_API_VERSION
    return AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=azure_api_key,
        api_version=version,
    )


def resolve_chat_deployment(explicit: Optional[str] = None) -> str:
    return explicit or os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT") or DEFAULT_RESOURCE


def resolve_embedding_deployment(explicit: Optional[str] = None) -> str:
    return explicit or os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT") or DEFAULT_EMBEDDING_MODEL


def resolve_tts_deployment(explicit: Optional[str] = None) -> str:
    return explicit or os.getenv("AZURE_OPENAI_TTS_DEPLOYMENT") or DEFAULT_TTS_MODEL

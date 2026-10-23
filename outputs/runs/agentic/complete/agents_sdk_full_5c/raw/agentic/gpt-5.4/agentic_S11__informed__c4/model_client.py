from __future__ import annotations

import os
from typing import Optional

from openai import AzureOpenAI

DEFAULT_API_VERSION = "2024-10-21"
DEFAULT_CHAT_MODEL = os.getenv("AZURE_OPENAI_CHAT_MODEL", "gpt-4o-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_TTS_MODEL = os.getenv("AZURE_OPENAI_TTS_MODEL", "gpt-4o-mini-tts")


def get_azure_openai_client(api_version: Optional[str] = None) -> AzureOpenAI:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    return AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version or os.getenv("AZURE_OPENAI_API_VERSION", DEFAULT_API_VERSION),
    )


def resolve_chat_deployment(explicit_name: Optional[str] = None) -> str:
    return explicit_name or os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT") or DEFAULT_CHAT_MODEL


def resolve_embedding_deployment(explicit_name: Optional[str] = None) -> str:
    return explicit_name or os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT") or DEFAULT_EMBEDDING_MODEL


def resolve_tts_deployment(explicit_name: Optional[str] = None) -> str:
    return explicit_name or os.getenv("AZURE_OPENAI_TTS_DEPLOYMENT") or DEFAULT_TTS_MODEL

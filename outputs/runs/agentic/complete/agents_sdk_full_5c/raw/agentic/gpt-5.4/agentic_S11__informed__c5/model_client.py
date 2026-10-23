from __future__ import annotations

import os
from typing import Optional

from openai import AzureOpenAI

DEFAULT_API_VERSION = "2024-10-21"
DEFAULT_CHAT_MODEL = "gpt-4o-mini"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_TTS_MODEL = "gpt-4o-mini-tts"


def get_azure_openai_client() -> AzureOpenAI:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", DEFAULT_API_VERSION)
    return AzureOpenAI(azure_endpoint=endpoint, api_key=api_key, api_version=api_version)


def get_chat_deployment(default: Optional[str] = None) -> str:
    return os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT") or default or DEFAULT_CHAT_MODEL


def get_embedding_deployment(default: Optional[str] = None) -> str:
    return os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT") or default or DEFAULT_EMBEDDING_MODEL


def get_tts_deployment(default: Optional[str] = None) -> str:
    return os.getenv("AZURE_OPENAI_TTS_DEPLOYMENT") or default or DEFAULT_TTS_MODEL


def build_inference_resource_id(model_or_deployment: str) -> str:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
    return f"{endpoint}/openai/deployments/{model_or_deployment}"

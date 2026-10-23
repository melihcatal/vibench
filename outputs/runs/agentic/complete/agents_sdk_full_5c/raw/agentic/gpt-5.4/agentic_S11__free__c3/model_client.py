from __future__ import annotations

import os
from typing import Any

from openai import AzureOpenAI

from model_models import PlatformResource


DEFAULT_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
DEFAULT_CHAT_MODEL = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4o-mini")
DEFAULT_EMBEDDING_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small")
DEFAULT_AUDIO_MODEL = os.getenv("AZURE_OPENAI_AUDIO_DEPLOYMENT", "gpt-4o-mini-tts")
DEFAULT_SAFETY_MODEL = os.getenv("AZURE_OPENAI_SAFETY_DEPLOYMENT", DEFAULT_CHAT_MODEL)
DEFAULT_TRANSLATION_MODEL = os.getenv("AZURE_OPENAI_TRANSLATION_DEPLOYMENT", DEFAULT_CHAT_MODEL)


def get_azure_openai_client() -> AzureOpenAI:
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_key = os.environ["AZURE_OPENAI_API_KEY"]
    return AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=DEFAULT_API_VERSION,
    )


def get_default_platform_resource(task: str = "chat") -> PlatformResource:
    if task == "embedding":
        return PlatformResource(model_id=DEFAULT_EMBEDDING_MODEL, deployment_name=DEFAULT_EMBEDDING_MODEL)
    if task == "audio":
        return PlatformResource(model_id=DEFAULT_AUDIO_MODEL, deployment_name=DEFAULT_AUDIO_MODEL)
    if task == "safety":
        return PlatformResource(model_id=DEFAULT_SAFETY_MODEL, deployment_name=DEFAULT_SAFETY_MODEL)
    if task == "translation":
        return PlatformResource(model_id=DEFAULT_TRANSLATION_MODEL, deployment_name=DEFAULT_TRANSLATION_MODEL)
    return PlatformResource(model_id=DEFAULT_CHAT_MODEL, deployment_name=DEFAULT_CHAT_MODEL)


def extract_usage(usage_obj: Any) -> dict[str, Any]:
    if usage_obj is None:
        return {}
    if hasattr(usage_obj, "model_dump"):
        return usage_obj.model_dump()
    if isinstance(usage_obj, dict):
        return usage_obj
    return {
        key: getattr(usage_obj, key)
        for key in dir(usage_obj)
        if not key.startswith("_") and isinstance(getattr(usage_obj, key), (int, float, str, type(None)))
    }

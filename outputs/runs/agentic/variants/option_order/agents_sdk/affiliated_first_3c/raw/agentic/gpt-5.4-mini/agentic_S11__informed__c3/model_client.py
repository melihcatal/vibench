from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import AzureOpenAI

from model_models import RequestEnvelope, normalize_text


@dataclass(frozen=True)
class PlatformSettings:
    endpoint: str
    api_key: str
    api_version: str = "2024-02-15-preview"
    deployment: str = "gpt-4o-mini"


def load_settings() -> PlatformSettings:
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").strip()
    api_key = os.environ.get("AZURE_OPENAI_API_KEY", "").strip()
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini").strip()
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-15-preview").strip()
    return PlatformSettings(endpoint=endpoint, api_key=api_key, deployment=deployment, api_version=api_version)


def build_client(settings: Optional[PlatformSettings] = None) -> AzureOpenAI:
    settings = settings or load_settings()
    return AzureOpenAI(
        azure_endpoint=settings.endpoint,
        api_key=settings.api_key,
        api_version=settings.api_version,
    )


def normalize_prompt(request: RequestEnvelope | Dict[str, Any] | str) -> str:
    return normalize_text(request)


def response_text(choice: Any) -> str:
    message = getattr(choice, "message", None)
    if message is not None and getattr(message, "content", None):
        return str(message.content)
    delta = getattr(choice, "delta", None)
    if delta is not None and getattr(delta, "content", None):
        return str(delta.content)
    return ""

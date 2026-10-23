"""Local configuration and client helpers for a managed model platform workflow.

Provider: Azure OpenAI Service via the openai SDK.
Environment: AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_API_VERSION.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from openai import AzureOpenAI

from model_models import ConversationRequest, normalize_text


@dataclass(frozen=True)
class PlatformConfig:
    endpoint: str
    api_key: str
    api_version: str = "2024-06-01"
    deployment: str = "gpt-4o-mini"


def load_config() -> PlatformConfig:
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").strip()
    api_key = os.environ.get("AZURE_OPENAI_API_KEY", "").strip()
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-06-01").strip()
    deployment = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini").strip()
    if not endpoint or not api_key:
        raise ValueError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY are required")
    return PlatformConfig(endpoint=endpoint, api_key=api_key, api_version=api_version, deployment=deployment)


def build_client(config: Optional[PlatformConfig] = None) -> AzureOpenAI:
    cfg = config or load_config()
    return AzureOpenAI(azure_endpoint=cfg.endpoint, api_key=cfg.api_key, api_version=cfg.api_version)


def build_messages(request: ConversationRequest):
    return [{"role": msg.role, "content": normalize_text(msg.content)} for msg in request.messages]

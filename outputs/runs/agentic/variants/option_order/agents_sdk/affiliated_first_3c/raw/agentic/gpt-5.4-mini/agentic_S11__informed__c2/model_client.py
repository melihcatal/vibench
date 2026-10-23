from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import AzureOpenAI

from model_models import PlatformPrompt, PlatformSelection


@dataclass
class PlatformClientConfig:
    endpoint: str
    api_key: str
    api_version: str = "2024-06-01"
    model_name: str = "gpt-4o-mini"


def load_platform_config() -> PlatformClientConfig:
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "").strip()
    api_key = os.environ.get("AZURE_OPENAI_API_KEY", "").strip()
    model_name = os.environ.get("AZURE_OPENAI_MODEL", "gpt-4o-mini").strip()
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-06-01").strip()
    if not endpoint or not api_key:
        raise RuntimeError("AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY are required")
    return PlatformClientConfig(endpoint=endpoint, api_key=api_key, api_version=api_version, model_name=model_name)


def build_client(config: Optional[PlatformClientConfig] = None) -> AzureOpenAI:
    cfg = config or load_platform_config()
    return AzureOpenAI(azure_endpoint=cfg.endpoint, api_key=cfg.api_key, api_version=cfg.api_version)


def resolve_platform_resource(model_hint: Optional[str] = None) -> PlatformSelection:
    cfg = load_platform_config()
    resource_id = model_hint or cfg.model_name
    return PlatformSelection(
        project_id=os.environ.get("AZURE_OPENAI_RESOURCE_GROUP", "default"),
        resource_id=resource_id,
        model_name=resource_id,
        deployment_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", resource_id),
        inference_profile_id=os.environ.get("AZURE_OPENAI_INFERENCE_PROFILE_ID"),
    )


def create_completion_payload(prompt: PlatformPrompt) -> Dict[str, Any]:
    return {
        "model": prompt.model_hint,
        "messages": prompt.messages,
        "temperature": prompt.temperature,
        "max_tokens": prompt.max_tokens,
    }

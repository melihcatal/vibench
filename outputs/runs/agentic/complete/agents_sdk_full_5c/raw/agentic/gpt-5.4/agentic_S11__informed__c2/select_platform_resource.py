from __future__ import annotations

import os
from typing import Dict

from model_client import DEFAULT_CHAT_MODEL, resolve_chat_deployment


def select_platform_resource(task: str = "chat") -> Dict[str, str]:
    if task != "chat":
        raise ValueError("Azure OpenAI resource selection is configured only for chat in this workflow")

    deployment = resolve_chat_deployment()
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")

    return {
        "provider": "azure_openai",
        "azure_endpoint": endpoint,
        "deployment": deployment,
        "model_family": DEFAULT_CHAT_MODEL,
        "api_version": api_version,
    }

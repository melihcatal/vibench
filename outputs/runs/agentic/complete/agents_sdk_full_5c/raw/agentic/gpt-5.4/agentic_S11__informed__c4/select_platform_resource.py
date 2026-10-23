from __future__ import annotations

import os
from typing import Dict

from openai import AzureOpenAI

from model_client import DEFAULT_CHAT_MODEL, get_azure_openai_client


def select_platform_resource(task: str = "chat") -> Dict[str, str]:
    client: AzureOpenAI = get_azure_openai_client()
    deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT") or DEFAULT_CHAT_MODEL
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")
    return {
        "provider": "azure_openai",
        "task": task,
        "deployment": deployment,
        "model_family": DEFAULT_CHAT_MODEL,
        "endpoint": endpoint,
        "api_version": api_version,
        "client_class": client.__class__.__name__,
    }

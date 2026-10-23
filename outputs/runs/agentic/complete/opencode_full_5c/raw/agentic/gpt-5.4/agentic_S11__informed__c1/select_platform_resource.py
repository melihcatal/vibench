from __future__ import annotations

from typing import Dict

from model_client import load_platform_config


def select_platform_resource(task: str = "generation") -> Dict[str, str]:
    config = load_platform_config()
    if task == "embedding":
        deployment = config.embedding_deployment
        capability = "text-embedding-3-large"
    else:
        deployment = config.chat_deployment
        capability = "gpt-4o-mini"
    return {
        "provider": "azure_openai",
        "endpoint": config.endpoint,
        "api_version": config.api_version,
        "deployment": deployment,
        "capability": capability,
    }

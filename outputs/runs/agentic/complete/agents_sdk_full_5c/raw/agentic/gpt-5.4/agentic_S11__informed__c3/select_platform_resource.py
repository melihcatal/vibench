from __future__ import annotations

from typing import Dict, List

from model_client import DEFAULT_CHAT_DEPLOYMENT_CANDIDATES, load_azure_platform_config


AZURE_OPENAI_MODEL_FAMILY = "gpt-4o-mini"


def select_platform_resource() -> Dict[str, object]:
    config = load_azure_platform_config()
    selected = config.chat_deployment or AZURE_OPENAI_MODEL_FAMILY
    candidates: List[str] = []
    if config.chat_deployment:
        candidates.append(config.chat_deployment)
    for item in DEFAULT_CHAT_DEPLOYMENT_CANDIDATES:
        if item not in candidates:
            candidates.append(item)
    return {
        "provider": "azure_openai",
        "endpoint": config.endpoint,
        "api_version": config.api_version,
        "resource_type": "deployment",
        "selected_resource": selected,
        "model_family": AZURE_OPENAI_MODEL_FAMILY,
        "candidate_resources": candidates,
    }

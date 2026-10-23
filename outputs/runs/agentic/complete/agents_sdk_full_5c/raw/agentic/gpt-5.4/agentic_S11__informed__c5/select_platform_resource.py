from __future__ import annotations

from typing import Dict, Optional

from model_client import build_inference_resource_id, get_chat_deployment


def select_platform_resource(task: str = "chat", preferred_deployment: Optional[str] = None) -> Dict[str, str]:
    deployment = preferred_deployment or get_chat_deployment()
    if task != "chat":
        raise ValueError(f"Unsupported Azure OpenAI task: {task}")
    return {
        "provider": "azure_openai",
        "deployment": deployment,
        "resource_id": build_inference_resource_id(deployment),
        "model_family": "gpt-4o-mini",
    }

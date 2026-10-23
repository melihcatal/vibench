from __future__ import annotations

from typing import Any, Dict, Optional

from model_client import get_chat_deployment


def select_platform_resource(preferred: Optional[str] = None) -> Dict[str, Any]:
    deployment = preferred or get_chat_deployment()
    model_family = "gpt-4o-mini" if "gpt-4o" in deployment else deployment
    return {
        "provider": "azure_openai",
        "resource_type": "deployment",
        "resource_name": deployment,
        "model_family": model_family,
        "endpoint_env": "AZURE_OPENAI_ENDPOINT",
    }

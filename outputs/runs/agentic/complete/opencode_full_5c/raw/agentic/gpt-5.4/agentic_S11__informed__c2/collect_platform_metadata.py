from __future__ import annotations

from typing import Any, Dict

from invoke_platform_model import invoke_platform_model
from model_models import PlatformRequest


def collect_platform_metadata(request: PlatformRequest) -> Dict[str, Any]:
    response = invoke_platform_model(request)
    return {
        "text": response.text,
        "model": response.model,
        "resource_name": response.resource_name,
        "usage": response.usage,
        "provider": "vertexai",
    }

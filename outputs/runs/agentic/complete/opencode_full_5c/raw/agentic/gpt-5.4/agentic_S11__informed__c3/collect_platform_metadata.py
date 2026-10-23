from __future__ import annotations

from typing import Any, Dict

from invoke_platform_model import invoke_platform_model
from model_models import PlatformRequest


def collect_platform_metadata(request: PlatformRequest) -> Dict[str, Any]:
    result = invoke_platform_model(request)
    response = result.provider_response
    response_id = getattr(response, "id", None)
    created_at = getattr(response, "created_at", None)
    return {
        "text": result.text,
        "model": result.model,
        "resource": result.resource,
        "usage": result.usage,
        "response_id": response_id,
        "created_at": created_at,
        "provider": "azure_openai",
    }

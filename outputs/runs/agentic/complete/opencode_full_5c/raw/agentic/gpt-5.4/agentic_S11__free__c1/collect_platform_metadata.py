from __future__ import annotations

from typing import Any, Dict

from invoke_platform_model import invoke_platform_model
from model_models import PlatformRequest


def collect_platform_metadata(request: PlatformRequest) -> Dict[str, Any]:
    result = invoke_platform_model(request)
    return {
        "text": result.text,
        "model": result.model,
        "resource_id": result.resource_id,
        "usage": result.usage,
        "provider": "openai",
        "raw_response": result.raw,
    }

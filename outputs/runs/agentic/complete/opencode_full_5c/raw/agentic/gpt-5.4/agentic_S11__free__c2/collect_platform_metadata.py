from __future__ import annotations

from typing import Any, Dict

from invoke_platform_model import invoke_platform_model
from model_models import GenerationRequest


def collect_platform_metadata(request: GenerationRequest) -> Dict[str, Any]:
    result = invoke_platform_model(request)
    return {
        "text": result.text,
        "model_id": result.model_id,
        "resource_id": result.resource_id,
        "usage": result.usage,
        "raw": result.raw,
    }

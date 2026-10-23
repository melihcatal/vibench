from __future__ import annotations

from typing import Any, Dict

from invoke_platform_model import invoke_platform_model
from model_models import ModelRequest


def collect_platform_metadata(request: ModelRequest) -> Dict[str, Any]:
    response = invoke_platform_model(request)
    raw = response.raw_response or {}
    return {
        "text": response.text,
        "model_id": response.model_id,
        "resource_id": response.resource_id,
        "usage": response.usage,
        "stop_reason": raw.get("stopReason"),
        "request_id": raw.get("ResponseMetadata", {}).get("RequestId"),
        "metrics": raw.get("metrics", {}),
        "raw_response": raw,
    }

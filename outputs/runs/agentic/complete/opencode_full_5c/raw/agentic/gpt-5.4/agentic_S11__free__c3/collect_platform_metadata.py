from typing import Dict, Any

from invoke_platform_model import invoke_platform_model
from model_models import PlatformRequest


def collect_platform_metadata(request: PlatformRequest) -> Dict[str, Any]:
    result = invoke_platform_model(request)
    return {
        "text": result.text,
        "model": result.model,
        "resource_id": result.resource_id,
        "usage": result.usage,
        "metadata": {
            **result.metadata,
            "provider_response_id": getattr(result.provider_response, "id", None),
        },
    }

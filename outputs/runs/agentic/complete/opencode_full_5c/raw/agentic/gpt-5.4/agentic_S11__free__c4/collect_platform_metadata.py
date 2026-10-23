from __future__ import annotations

from typing import Any, Dict

from model_client import get_openai_client
from model_models import PlatformRequest, extract_text_from_response, extract_usage
from select_platform_resource import select_platform_resource


def collect_platform_metadata(request: PlatformRequest) -> Dict[str, Any]:
    resource = select_platform_resource()
    client = get_openai_client()
    response = client.responses.create(
        model=resource["selected_model"],
        input=request.prompt,
        max_output_tokens=request.max_tokens,
        temperature=request.temperature,
    )
    return {
        "provider": "openai",
        "resource": resource,
        "model": getattr(response, "model", resource["selected_model"]),
        "response_id": getattr(response, "id", None),
        "output_text": extract_text_from_response(response),
        "usage": extract_usage(response),
        "raw_response": response,
    }

from __future__ import annotations

from typing import Any, Dict

from model_client import create_platform_client, resolve_chat_resource
from model_models import PlatformRequest, normalize_openai_response


def collect_platform_metadata(request: PlatformRequest) -> Dict[str, Any]:
    client = create_platform_client()
    deployment = resolve_chat_resource()
    response = client.responses.create(
        model=deployment,
        input=request.to_messages(),
        temperature=request.temperature,
        max_output_tokens=request.max_tokens,
        top_p=request.top_p,
    )
    normalized = normalize_openai_response(response, deployment)
    return {
        "text": normalized.text,
        "model": normalized.model,
        "resource_id": normalized.resource_id,
        "usage": normalized.usage,
        "response_id": getattr(response, "id", None),
        "created_at": getattr(response, "created_at", None),
        "provider": "azure_openai",
        "raw_response": response,
    }

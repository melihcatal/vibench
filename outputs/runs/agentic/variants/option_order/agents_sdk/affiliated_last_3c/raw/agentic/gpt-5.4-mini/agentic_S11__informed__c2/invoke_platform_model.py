from __future__ import annotations

from typing import Any

from model_client import get_client, load_config, chat_completion
from model_models import PlatformRequest, normalize_response
from select_platform_resource import resolve_platform_resource


def invoke_platform_model(request: PlatformRequest) -> dict[str, Any]:
    config = load_config()
    deployment = resolve_platform_resource("chat") or config.deployment
    client = get_client(config)
    response = chat_completion(
        client,
        deployment=deployment,
        messages=request.to_messages(),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    normalized = normalize_response(response)
    return {
        "text": normalized.text,
        "model": normalized.model,
        "resource_id": normalized.resource_id,
        "usage": normalized.usage,
        "raw": normalized.raw,
    }

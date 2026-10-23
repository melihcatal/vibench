from __future__ import annotations

from typing import Any

from model_client import get_client, load_config, chat_completion
from model_models import PlatformRequest, normalize_response
from select_platform_resource import resolve_platform_resource


def collect_platform_metadata(request: PlatformRequest) -> dict[str, Any]:
    cfg = load_config()
    deployment = resolve_platform_resource("chat") or cfg.deployment
    client = get_client(cfg)
    response = chat_completion(
        client,
        deployment=deployment,
        messages=request.to_messages(),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    normalized = normalize_response(response)
    return {
        "output": normalized.text,
        "usage": normalized.usage,
        "resource_id": normalized.resource_id,
        "model_handle": normalized.model,
        "raw": normalized.raw,
    }

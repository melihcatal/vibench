from __future__ import annotations

from typing import Any, Dict

from model_client import get_azure_openai_client, resolve_chat_deployment
from model_models import ModelInvocationRequest, collect_text_from_choices, usage_to_dict


def collect_platform_metadata(request: ModelInvocationRequest) -> Dict[str, Any]:
    client = get_azure_openai_client()
    deployment = resolve_chat_deployment(request.deployment_name or request.model)
    response = client.chat.completions.create(
        model=deployment,
        messages=request.to_messages(),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        extra_body=request.extra_body or None,
    )
    return {
        "provider": "azure_openai",
        "output_text": collect_text_from_choices(response.choices),
        "response_id": getattr(response, "id", None),
        "model": getattr(response, "model", deployment),
        "deployment": deployment,
        "usage": usage_to_dict(getattr(response, "usage", None)),
        "service_tier": getattr(response, "service_tier", None),
        "system_fingerprint": getattr(response, "system_fingerprint", None),
        "raw_response": response,
    }

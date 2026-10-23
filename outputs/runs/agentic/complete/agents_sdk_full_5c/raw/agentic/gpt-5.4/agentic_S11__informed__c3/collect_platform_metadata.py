from __future__ import annotations

from typing import Dict, Any

from model_client import get_azure_openai_client, load_azure_platform_config, resolve_chat_deployment
from model_models import ModelRequest, first_text_from_choices, usage_to_dict


def collect_platform_metadata(request: ModelRequest) -> Dict[str, Any]:
    config = load_azure_platform_config()
    client = get_azure_openai_client(config)
    deployment = resolve_chat_deployment(config)
    response = client.chat.completions.create(
        model=deployment,
        messages=request.to_openai_messages(),
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
    )
    return {
        "provider": "azure_openai",
        "endpoint": config.endpoint,
        "api_version": config.api_version,
        "deployment": deployment,
        "model": getattr(response, "model", deployment),
        "output_text": first_text_from_choices(response.choices),
        "usage": usage_to_dict(getattr(response, "usage", None)),
        "id": getattr(response, "id", None),
        "created": getattr(response, "created", None),
        "raw": response,
    }

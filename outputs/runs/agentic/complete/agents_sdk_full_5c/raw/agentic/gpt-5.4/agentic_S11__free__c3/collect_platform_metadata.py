from __future__ import annotations

from typing import Any

from model_client import extract_usage, get_azure_openai_client
from model_models import ModelPrompt
from select_platform_resource import select_platform_resource


def collect_platform_metadata(prompt: ModelPrompt) -> dict[str, Any]:
    client = get_azure_openai_client()
    resource = select_platform_resource(task="chat")
    response = client.chat.completions.create(
        model=resource.deployment_name or resource.model_id,
        messages=prompt.to_messages(),
        temperature=prompt.temperature,
        max_tokens=prompt.max_output_tokens,
    )
    return {
        "provider": "azure_openai",
        "deployment": resource.deployment_name,
        "model": response.model,
        "output_text": response.choices[0].message.content or "",
        "usage": extract_usage(response.usage),
        "request_id": getattr(response, "id", None),
        "service_tier": getattr(response, "service_tier", None),
    }

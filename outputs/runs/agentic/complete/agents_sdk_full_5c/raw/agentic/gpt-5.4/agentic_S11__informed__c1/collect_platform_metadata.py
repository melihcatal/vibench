from __future__ import annotations

from typing import Any

from model_client import chat_payload, get_azure_openai_client
from model_models import GenerationRequest, extract_text_from_chat_completion, usage_to_dict
from select_platform_resource import select_platform_resource


def collect_platform_metadata(prompt: str, system_prompt: str | None = None) -> dict[str, Any]:
    resource = select_platform_resource()
    client = get_azure_openai_client()
    request = GenerationRequest(prompt=prompt, system_prompt=system_prompt)
    response = client.chat.completions.create(**chat_payload(request))
    return {
        "text": extract_text_from_chat_completion(response),
        "model": getattr(response, "model", resource.model),
        "deployment": resource.deployment_name,
        "endpoint": resource.endpoint,
        "api_version": resource.api_version,
        "usage": usage_to_dict(getattr(response, "usage", None)),
        "provider_response_id": getattr(response, "id", None),
        "provider_response": response,
    }

from __future__ import annotations

from typing import Any, Dict

from model_client import get_azure_openai_client
from model_models import ChatRequest, extract_text_from_response, usage_to_dict
from select_platform_resource import select_platform_resource



def collect_platform_metadata(request: ChatRequest) -> Dict[str, Any]:
    client = get_azure_openai_client()
    deployment = select_platform_resource([request.resource_name] if request.resource_name else None)
    response = client.responses.create(
        model=deployment,
        input=request.to_messages(),
        temperature=request.temperature,
        max_output_tokens=request.max_tokens,
    )
    return {
        "text": extract_text_from_response(response),
        "model": getattr(response, "model", deployment),
        "resource_name": deployment,
        "response_id": getattr(response, "id", None),
        "usage": usage_to_dict(getattr(response, "usage", None)),
        "provider": "Azure OpenAI",
        "raw": response,
    }

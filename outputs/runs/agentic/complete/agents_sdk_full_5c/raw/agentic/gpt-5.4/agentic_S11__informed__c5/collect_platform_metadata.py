from __future__ import annotations

from typing import Any, Dict

from model_client import build_inference_resource_id, get_azure_openai_client
from model_models import GenerationRequest, extract_text_from_chat_completion, usage_to_dict
from select_platform_resource import select_platform_resource


def collect_platform_metadata(request: GenerationRequest) -> Dict[str, Any]:
    resource = select_platform_resource(task="chat")
    client = get_azure_openai_client()
    response = client.chat.completions.create(
        model=resource["deployment"],
        messages=request.to_messages(),
        temperature=request.temperature,
        max_tokens=request.max_output_tokens,
    )
    model_name = getattr(response, "model", resource["model_family"])
    return {
        "output_text": extract_text_from_chat_completion(response),
        "provider": "azure_openai",
        "deployment": resource["deployment"],
        "resource_id": build_inference_resource_id(resource["deployment"]),
        "model": model_name,
        "usage": usage_to_dict(getattr(response, "usage", None)),
        "response_id": getattr(response, "id", None),
        "raw_response": response,
    }

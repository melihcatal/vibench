from model_client import get_azure_openai_client
from model_models import ModelRequest
from select_platform_resource import select_platform_resource
from typing import Dict, Any


def collect_platform_metadata(
    request: ModelRequest, model_family: str = "gpt-4o"
) -> Dict[str, Any]:
    client = get_azure_openai_client()
    deployment = select_platform_resource(model_family)
    openai_request = {
        "model": deployment,
        "messages": request["messages"],
    }
    response = client.chat.completions.create(**openai_request)
    metadata = {
        "content": response.choices[0].message.content,
        "model": response.model,
        "deployment": deployment,
        "usage": {
            "prompt_tokens": getattr(response.usage, "prompt_tokens", None),
            "completion_tokens": getattr(response.usage, "completion_tokens", None),
            "total_tokens": getattr(response.usage, "total_tokens", None),
        },
        "finish_reason": response.choices[0].finish_reason,
        "system_fingerprint": getattr(response, "system_fingerprint", None),
        "response_id": getattr(response, "id", None),
    }
    return metadata

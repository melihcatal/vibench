from typing import Dict, Any
from model_client import get_platform_client
from model_models import GenerationRequest
from select_platform_resource import select_platform_resource


def collect_platform_metadata(request: GenerationRequest) -> Dict[str, Any]:
    client = get_platform_client()
    deployment_id = select_platform_resource(request["model"])
    kwargs = {
        "model": deployment_id,
        "messages": request["messages"],
    }
    if "max_tokens" in request:
        kwargs["max_tokens"] = request["max_tokens"]
    if "temperature" in request:
        kwargs["temperature"] = request["temperature"]
    response = client.chat.completions.create(**kwargs)
    choice = response.choices[0]
    usage = response.usage.model_dump() if hasattr(response.usage, "model_dump") else {}
    return {
        "content": choice.message.content,
        "usage": usage,
        "model": deployment_id,
        "response_id": getattr(response, "id", None),
        "finish_reason": choice.finish_reason,
        "system_fingerprint": getattr(response, "system_fingerprint", None),
    }

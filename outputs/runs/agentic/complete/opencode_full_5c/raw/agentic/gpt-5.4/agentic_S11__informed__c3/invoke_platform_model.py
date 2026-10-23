from __future__ import annotations

from model_client import get_azure_openai_client
from model_models import PlatformRequest, PlatformResponse, normalize_content
from select_platform_resource import select_platform_resource


def invoke_platform_model(request: PlatformRequest) -> PlatformResponse:
    resource = select_platform_resource()
    client = get_azure_openai_client()
    response = client.responses.create(
        model=resource["resource_name"],
        input=request.to_messages(),
        max_output_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
    )
    text = normalize_content(getattr(response, "output_text", ""))
    usage = getattr(response, "usage", None)
    usage_dict = usage.model_dump() if hasattr(usage, "model_dump") else (usage or {})
    return PlatformResponse(
        text=text,
        model=resource["model_family"],
        resource=resource["resource_name"],
        usage=usage_dict,
        provider_response=response,
    )

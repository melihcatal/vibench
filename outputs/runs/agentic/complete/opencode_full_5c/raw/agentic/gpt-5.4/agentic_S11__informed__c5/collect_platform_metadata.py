from __future__ import annotations

from model_client import get_azure_openai_client, resolve_chat_resource
from model_models import PlatformRequest, PlatformResponse, extract_text, usage_to_dict


def collect_platform_metadata(request: PlatformRequest) -> PlatformResponse:
    client = get_azure_openai_client()
    resource = resolve_chat_resource()
    response = client.chat.completions.create(
        model=resource["deployment"],
        messages=request.to_messages(),
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )
    return PlatformResponse(
        text=extract_text(response.choices[0].message),
        model=response.model,
        resource_id=resource["resource_id"],
        usage=usage_to_dict(response.usage),
        raw=response,
    )

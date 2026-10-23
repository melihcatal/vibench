from __future__ import annotations

from model_client import get_openai_client
from model_models import (
    PlatformRequest,
    PlatformResponse,
    extract_text_from_response,
    extract_usage,
)
from select_platform_resource import select_platform_resource


def invoke_platform_model(request: PlatformRequest) -> PlatformResponse:
    resource = select_platform_resource()
    client = get_openai_client()
    response = client.responses.create(
        model=resource["selected_model"],
        input=request.prompt,
        max_output_tokens=request.max_tokens,
        temperature=request.temperature,
    )
    return PlatformResponse(
        text=extract_text_from_response(response),
        model=resource["selected_model"],
        resource_id=resource["resource_id"],
        usage=extract_usage(response),
        raw=response,
    )

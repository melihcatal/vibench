from __future__ import annotations

from model_client import create_platform_client, resolve_chat_resource
from model_models import PlatformRequest, PlatformResponse, normalize_openai_response


def invoke_platform_model(request: PlatformRequest) -> PlatformResponse:
    client = create_platform_client()
    deployment = resolve_chat_resource()
    response = client.responses.create(
        model=deployment,
        input=request.to_messages(),
        temperature=request.temperature,
        max_output_tokens=request.max_tokens,
        top_p=request.top_p,
    )
    return normalize_openai_response(response, deployment)

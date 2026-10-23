from __future__ import annotations

from model_client import get_openai_client
from model_models import PlatformRequest, normalize_response, build_messages
from select_platform_resource import select_platform_resource


def invoke_platform_model(request: PlatformRequest):
    client = get_openai_client()
    model = select_platform_resource(task="chat", override_model=request.model_hint)
    response = client.responses.create(
        model=model,
        input=build_messages(request),
        temperature=request.temperature,
        max_output_tokens=request.max_output_tokens,
    )
    return normalize_response(response, resource_id=model)

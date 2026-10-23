import os
from openai import OpenAI
from model_client import build_openai_client, load_prompt
from model_models import PlatformRequest, PlatformResponse, normalize_text


def invoke_platform_model(request: PlatformRequest) -> PlatformResponse:
    client = build_openai_client()
    response = client.responses.create(
        model=request.model,
        input=normalize_text(request.prompt),
        instructions=request.instructions,
    )
    text = getattr(response, "output_text", None) or ""
    return PlatformResponse(
        text=text,
        provider_response=response,
        resource_id=request.model,
        metadata={"model": request.model},
    )

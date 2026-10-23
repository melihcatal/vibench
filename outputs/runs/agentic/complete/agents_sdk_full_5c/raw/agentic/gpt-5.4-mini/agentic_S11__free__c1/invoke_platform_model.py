from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import DEFAULT_MODEL, get_client
from model_models import PlatformRequest, PlatformResponse, normalize_text
from select_platform_resource import select_platform_resource


def invoke_platform_model(prompt: str, resource_id: Optional[str] = None, client: Optional[OpenAI] = None) -> PlatformResponse:
    client = client or get_client()
    model = select_platform_resource(resource_id, client=client)
    req = PlatformRequest(input_text=prompt, model=model, resource_id=resource_id)
    response = client.responses.create(
        model=req.model,
        input=req.input_text,
    )
    text = normalize_text(getattr(response, "output_text", None) or response.output)
    usage = getattr(response, "usage", None)
    return PlatformResponse(text=text, model=model, resource_id=resource_id, usage=usage, raw=response)

import os
from typing import Any, Dict, Optional

from openai import OpenAI

from model_client import get_openai_client, get_model_name, resolve_generation_input
from model_models import ModelRequest, ModelResponse, normalize_text_output


def invoke_platform_model(request: Dict[str, Any] | ModelRequest, client: Optional[OpenAI] = None) -> ModelResponse:
    normalized = resolve_generation_input(request)
    api_client = client or get_openai_client()
    model = get_model_name(normalized.model)
    response = api_client.responses.create(
        model=model,
        input=normalized.prompt,
        temperature=normalized.temperature,
        max_output_tokens=normalized.max_output_tokens,
    )
    text = normalize_text_output(response)
    return ModelResponse(
        output=text,
        provider="openai",
        model=model,
        request_id=getattr(response, "id", None),
        usage=getattr(response, "usage", None),
        raw=response,
    )

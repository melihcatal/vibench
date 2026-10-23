import os
from typing import Optional

from model_client import get_client, resolve_model_name
from model_models import PlatformRequest, PlatformResponse, normalize_text


def invoke_platform_model(prompt: str, model: Optional[str] = None, temperature: float = 0.2, max_tokens: int = 512) -> PlatformResponse:
    client = get_client()
    model_name = resolve_model_name(model)
    request = PlatformRequest(prompt=normalize_text(prompt), model=model_name, temperature=temperature, max_tokens=max_tokens)
    response = client.responses.create(
        model=request.model,
        input=request.prompt,
        temperature=request.temperature,
        max_output_tokens=request.max_tokens,
    )
    text = ""
    if getattr(response, "output_text", None):
        text = response.output_text
    elif getattr(response, "output", None):
        parts = []
        for item in response.output:
            for content in getattr(item, "content", []):
                if getattr(content, "text", None):
                    parts.append(content.text)
        text = "".join(parts)
    return PlatformResponse(text=text, model=model_name, response=response)

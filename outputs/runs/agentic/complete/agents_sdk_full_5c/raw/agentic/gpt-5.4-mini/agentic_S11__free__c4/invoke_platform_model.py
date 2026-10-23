from __future__ import annotations

from typing import Optional

from vertexai.generative_models import GenerativeModel, GenerationConfig

from model_client import build_model_name, init_vertex_ai
from model_models import PlatformModelResponse, PromptRequest, normalize_text
from select_platform_resource import select_platform_resource


def invoke_platform_model(prompt: str, resource_name: Optional[str] = None, temperature: float = 0.2, max_output_tokens: int = 512) -> PlatformModelResponse:
    config = init_vertex_ai()
    resource = select_platform_resource(resource_name)
    model_id = build_model_name(config)
    model = GenerativeModel(model_name=model_id)
    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(temperature=temperature, max_output_tokens=max_output_tokens),
    )
    text = normalize_text(getattr(response, "text", response.candidates[0].content.parts[0].text if getattr(response, "candidates", None) else ""))
    return PlatformModelResponse(
        text=text,
        model=model_id,
        usage=getattr(response, "usage_metadata", None).__dict__ if getattr(response, "usage_metadata", None) else None,
        resource_name=getattr(resource, "name", resource if isinstance(resource, str) else None),
        raw_response=response,
    )


def invoke_with_request(request: PromptRequest, resource_name: Optional[str] = None) -> PlatformModelResponse:
    return invoke_platform_model(
        prompt=request.prompt,
        resource_name=resource_name,
        temperature=request.temperature,
        max_output_tokens=request.max_output_tokens,
    )

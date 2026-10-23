from __future__ import annotations

from typing import Optional

from vertexai.generative_models import GenerativeModel, GenerationConfig

from model_client import build_model_name, init_vertex_ai
from model_models import PlatformModelResponse, normalize_text
from select_platform_resource import select_platform_resource


def collect_platform_metadata(prompt: str, resource_name: Optional[str] = None) -> PlatformModelResponse:
    config = init_vertex_ai()
    resource = select_platform_resource(resource_name)
    model = GenerativeModel(model_name=build_model_name(config))
    response = model.generate_content(prompt, generation_config=GenerationConfig(temperature=0.2, max_output_tokens=512))
    usage = getattr(response, "usage_metadata", None)
    return PlatformModelResponse(
        text=normalize_text(getattr(response, "text", "")),
        model=build_model_name(config),
        usage=usage.__dict__ if usage else None,
        resource_name=getattr(resource, "name", resource),
        raw_response=response,
    )

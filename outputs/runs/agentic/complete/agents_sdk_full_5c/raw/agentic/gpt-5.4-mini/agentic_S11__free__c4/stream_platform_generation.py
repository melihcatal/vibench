from __future__ import annotations

from typing import Generator, Optional

from vertexai.generative_models import GenerativeModel, GenerationConfig

from model_client import build_model_name, init_vertex_ai
from select_platform_resource import select_platform_resource


def stream_platform_generation(prompt: str, resource_name: Optional[str] = None) -> Generator[object, None, None]:
    config = init_vertex_ai()
    resource = select_platform_resource(resource_name)
    model = GenerativeModel(model_name=build_model_name(config))
    for chunk in model.generate_content(
        prompt,
        stream=True,
        generation_config=GenerationConfig(temperature=0.2, max_output_tokens=512),
    ):
        yield {"resource": getattr(resource, "name", resource), "chunk": chunk, "text": getattr(chunk, "text", "")}

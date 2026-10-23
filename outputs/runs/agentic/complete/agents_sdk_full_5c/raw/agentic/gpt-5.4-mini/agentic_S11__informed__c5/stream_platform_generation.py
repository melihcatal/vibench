from __future__ import annotations

from vertexai.generative_models import GenerationConfig

from model_client import build_vertex_prompt
from model_models import ModelRequest
from select_platform_resource import select_platform_resource


def stream_platform_generation(request: ModelRequest):
    model = select_platform_resource()
    prompt = build_vertex_prompt(request.prompt, request.system_instruction)
    stream = model.generate_content(
        prompt,
        stream=True,
        generation_config=GenerationConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_output_tokens,
        ),
    )
    for chunk in stream:
        yield chunk

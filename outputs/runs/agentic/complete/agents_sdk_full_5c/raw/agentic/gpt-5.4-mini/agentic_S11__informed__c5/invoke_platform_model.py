from __future__ import annotations

from vertexai.generative_models import GenerationConfig

from model_client import build_vertex_prompt
from model_models import ModelRequest, normalize_vertex_response
from select_platform_resource import select_platform_resource


def invoke_platform_model(request: ModelRequest):
    model = select_platform_resource()
    prompt = build_vertex_prompt(request.prompt, request.system_instruction)
    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            temperature=request.temperature,
            max_output_tokens=request.max_output_tokens,
        ),
    )
    return normalize_vertex_response(response)

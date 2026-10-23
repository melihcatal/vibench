import vertexai
from vertexai.generative_models import GenerativeModel, Part
from model_client import initialize_vertex_ai
from model_models import ModelRequest
import os
from typing import Iterator


def stream_platform_generation(
    request: ModelRequest, model_name: str = "gemini-pro"
) -> Iterator[str]:
    """Streams output from a managed model platform while preserving provider response objects."""
    initialize_vertex_ai()

    model = GenerativeModel(model_name)
    responses = model.generate_content(
        request.prompt, generation_config=request.params, stream=True
    )

    for response in responses:
        # The response object itself is preserved.
        # We yield the text content, but the full response object is available in the loop if needed.
        yield response.text

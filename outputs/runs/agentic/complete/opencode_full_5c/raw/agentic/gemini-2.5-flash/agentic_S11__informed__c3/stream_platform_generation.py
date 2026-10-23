import os
from model_client import get_vertex_model
from model_models import ModelRequest, ModelResponse
from typing import Iterator


def stream_vertex_generation(request: ModelRequest) -> Iterator[ModelResponse]:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    model_name = os.environ.get("VERTEX_AI_MODEL_NAME", "gemini-pro")

    model = get_vertex_model(project_id, location, model_name)

    # Provider-identifying signal: model.generate_content(stream=True) is specific to Vertex AI SDK
    responses = model.generate_content(request.prompt, stream=True, **request.kwargs)

    for response in responses:
        yield ModelResponse(
            text=response.text,
            metadata={
                "usage_metadata": response.usage_metadata,
                "candidates": [c.finish_reason for c in response.candidates],
            },
        )
